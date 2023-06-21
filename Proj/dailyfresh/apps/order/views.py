from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.http import JsonResponse
# Create your views here.
from django_redis import get_redis_connection
from django.db import transaction

from goods.models import GoodsSKU
from user.models import Address
from order.models import OrderInfo, OrderGoods
from utils.mixin import LoginRequiredMixin
from datetime import datetime
from alipay import AliPay
from dailyfresh import settings
import os


# /order/place/
class OrderPlaceView(LoginRequiredMixin, View):
    """订单页面"""
    def post(self, request):
        """订单页面显示"""
        user = request.user

        # 接收数据
        goods_id_list = request.POST.getlist('goods_id')

        # 数据校验
        if not goods_id_list:
            # 未传入要购买的商品
            return redirect(reverse('cart:show'))

        # 业务流程
        # 1. 获取每件商品的购买数目
        # 2. 计算商品的小计
        # 3. 计算商品的总件数，总价格
        # 4. 获取用户的收货地址
        conn = get_redis_connection('default')
        cart_key = 'cart_{}'.format(user.id)
        total_count = 0
        total_price = 0
        goods_list = []

        for goods_id in goods_id_list:
            goods = GoodsSKU.objects.get(id=goods_id)

            count = conn.hget(cart_key, goods_id)
            if count is None:
                return redirect(reverse('cart:show'))
            count = int(count)
            amount = count * goods.price

            goods.count = count
            goods.amount = amount

            total_count += count
            total_price += amount

            goods_list.append(goods)

        address = Address.objects.filter(user=user)

        # 运费, 写为固定值
        fare = 10
        pay_price = total_price + fare

        # 用于提交订单时，传递信息
        goods_id_str = ','.join(goods_id_list)

        context = {
            'total_price': total_price,
            'total_count': total_count,
            'goods_list': goods_list,
            'address': address,
            'fare': fare,
            'pay_price': pay_price,
            'goods_id_str': goods_id_str,
        }

        return render(request, 'place_order.html', context)


class OrderCommitView(View):
    """订单创建"""
    # 开启一个事务
    @transaction.atomic
    def post(self, request):
        """订单创建"""
        user = request.user

        if not user.is_authenticated():
            # 用户未登录
            return JsonResponse({'res': 0, 'errmsg': '用户未登录！'})

        addr_id = request.POST.get('addr_id')
        pay_style = request.POST.get('pay_style')
        goods_id_str = request.POST.get('goods_id_str')

        # 数据校验
        if not all([addr_id, pay_style, goods_id_str]):
            return JsonResponse({'res': 1, 'errmsg': '传入数据不足！'})

        if pay_style not in OrderInfo.PAY_METHOD.keys():
            # 支付方式不合法
            return JsonResponse({'res': 2, 'errmsg': '支付方式不合法！'})

        try:
            addr = Address.objects.get(id=addr_id)
        except Address.DoesNotExist:
            return JsonResponse({'res': 3, 'errmsg': '收货地址不存在！'})

        # 业务流程：创建订单
        # 订单ID，创建时间+用户ID
        order_id = datetime.now().strftime('%Y%m%d%H%M%S') + str(user.id)
        total_count = 0
        total_price = 0
        transit_price = 10

        # 创建一个事务保存点
        save_id = transaction.savepoint()

        try:
            # 添加订单信息表记录
            order_info = OrderInfo.objects.create(
                order_id=order_id,
                user=user,
                addr=addr,
                pay_method=pay_style,
                total_count=total_count,
                total_price=total_price,
                transit_price=transit_price,
            )

            conn = get_redis_connection('default')
            cart_key = 'cart_{}'.format(user.id)
            goods_id_list = goods_id_str.split(',')
            for goods_id in goods_id_list:
                # 乐观锁，
                # 不加锁，但是要利用循环，判断更新的库存和之前查出的库存是否一致
                for i in range(0, 3):
                    # 尝试3次
                    try:
                        goods = GoodsSKU.objects.get(id=goods_id)
                    except GoodsSKU.DoesNotExist:
                        # mysql事务回滚到 save_id 的事务保存点
                        transaction.savepoint_rollback(save_id)
                        return JsonResponse({'res': 4, 'errmsg': '商品不存在！'})

                    count = conn.hget(cart_key, goods.id)
                    count = int(count)

                    if count > goods.stock:
                        transaction.savepoint_rollback(save_id)
                        return JsonResponse({'res': 6, 'errmsg': '商品的库存不足！'})

                    # 更新商品的库存和销量
                    origin_stock = goods.stock
                    new_stock = origin_stock - count
                    new_sales = goods.sales + count

                    # 返回更新的条数，0代表更新失败，
                    res = GoodsSKU.objects.filter(id=goods_id, stock=origin_stock).update(stock=new_stock,
                                                                                          sales=new_sales)
                    if res == 0:
                        if i == 2:
                            # 尝试第三次
                            transaction.savepoint_rollback(save_id)
                            return JsonResponse({'res': 7, 'errmsg': '创建订单失败，库存不足！'})
                        continue

                    # 添加订单商品表记录
                    OrderGoods.objects.create(
                        order=order_info,
                        sku=goods,
                        count=count,
                        price=goods.price,
                    )

                    # 计算订单商品的总数量和总价格
                    amount = goods.price * count
                    total_count += count
                    total_price += amount

                    # 跳出循环
                    break

            # 更新订单信息表中的总数量和总价格记录
            order_info.total_count = total_count
            order_info.total_price = total_price
            order_info.save()
        except Exception as e:
            transaction.savepoint_rollback(save_id)
            return JsonResponse({'res': 7, 'errmsg': '创建订单失败'})

        # 提交事务
        transaction.savepoint_commit(save_id)

        # 清除用户购物车对应记录
        conn.hdel(cart_key, *goods_id_list)

        return JsonResponse({'res': 5, 'message': '订单创建成功！'})


# /order/commit/
class OrderCommitView1(View):
    """订单创建"""
    # 开启一个事务
    @transaction.atomic
    def post(self, request):
        """订单创建"""
        user = request.user

        if not user.is_authenticated():
            # 用户未登录
            return JsonResponse({'res': 0, 'errmsg': '用户未登录！'})

        addr_id = request.POST.get('addr_id')
        pay_style = request.POST.get('pay_style')
        goods_id_str = request.POST.get('goods_id_str')

        # 数据校验
        if not all([addr_id, pay_style, goods_id_str]):
            return JsonResponse({'res': 1, 'errmsg': '传入数据不足！'})

        if pay_style not in OrderInfo.PAY_METHOD.keys():
            # 支付方式不合法
            return JsonResponse({'res': 2, 'errmsg': '支付方式不合法！'})

        try:
            addr = Address.objects.get(id=addr_id)
        except Address.DoesNotExist:
            return JsonResponse({'res': 3, 'errmsg': '收货地址不存在！'})

        # 业务流程：创建订单
        # 订单ID，创建时间+用户ID
        order_id = datetime.now().strftime('%Y%m%d%H%M%S') + str(user.id)
        total_count = 0
        total_price = 0
        transit_price = 10

        # 创建一个事务保存点
        save_id = transaction.savepoint()

        try:
            # 添加订单信息表记录
            order_info = OrderInfo.objects.create(
                order_id=order_id,
                user=user,
                addr=addr,
                pay_method=pay_style,
                total_count=total_count,
                total_price=total_price,
                transit_price=transit_price,
            )

            conn = get_redis_connection('default')
            cart_key = 'cart_{}'.format(user.id)
            goods_id_list = goods_id_str.split(',')
            for goods_id in goods_id_list:
                try:
                    # goods = GoodsSKU.objects.get(id=goods_id)
                    # 解决订单并发，可能出现的库存不足的问题
                    # 悲观锁, 当一个用户拿到这个数据表后后，对这个数据表加锁，另一个用户不能对这个数据表进行更新操作
                    # select * from df_goods_sku where id=goods_id for update
                    goods = GoodsSKU.objects.select_for_update.get(id=goods_id)
                except GoodsSKU.DoesNotExist:
                    # mysql事务回滚到 save_id 的事务保存点
                    transaction.savepoint_rollback(save_id)
                    return JsonResponse({'res': 4, 'errmsg': '商品不存在！'})

                count = conn.hget(cart_key, goods.id)
                count = int(count)

                if count > goods.stock:
                    transaction.savepoint_rollback(save_id)
                    return JsonResponse({'res': 6, 'errmsg': '商品的库存不足！'})

                # 添加订单商品表记录
                OrderGoods.objects.create(
                    order=order_info,
                    sku=goods,
                    count=count,
                    price=goods.price,
                )

                # 更新商品的库存和销量
                goods.stock -= count
                goods.sales += count
                goods.save()

                # 计算订单商品的总数量和总价格
                amount = goods.price * count
                total_count += count
                total_price += amount

            # 更新订单信息表中的总数量和总价格记录
            order_info.total_count = total_count
            order_info.total_price = total_price
            order_info.save()
        except Exception as e:
            transaction.savepoint_rollback(save_id)
            return JsonResponse({'res': 7, 'errmsg': '创建订单失败'})

        # 提交事务
        transaction.savepoint_commit(save_id)

        # 清除用户购物车对应记录
        conn.hdel(cart_key, *goods_id_list)

        return JsonResponse({'res': 5, 'message': '订单创建成功！'})


# /order/pay/
class OrderPayView(View):
    """订单支付"""
    def post(self, request):
        user = request.user

        if not user.is_authenticated():
            # 用户未登录
            return redirect(reverse('user:login'))

        order_id = request.POST.get('order_id')
        if not order_id:
            return JsonResponse({'res': 1, 'errmsg': '未接收到数据！'})

        try:
            order = OrderInfo.objects.get(order_id=order_id,
                                          user=user,
                                          pay_method=3,
                                          order_status=1
                                          )
        except OrderInfo.DoesNotExist:
            return JsonResponse({'res': 2, 'errmsg': '订单不存在！'})

        app_private_key_string = open("./apps/order/app_private_key.pem").read()
        alipay_public_key_string = open("./apps/order/alipay_public_key.pem").read()

        alipay = AliPay(
            appid="2016092900627469",                  # app id
            app_notify_url=None,
            app_private_key_string=app_private_key_string,
            alipay_public_key_string=alipay_public_key_string,
            sign_type='RSA2',
            debug=True
        )

        subject = "天天生鲜订单{}".format(order.order_id)
        total_pay = order.total_price + order.transit_price

        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,          # 订单ID
            total_amount=str(total_pay),    # 订单总金额
            subject=subject,                # 订单主体
            return_url=None,
            notify_url=None
        )

        pay_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string
        return JsonResponse({'res': 3, 'pay_url': pay_url})


# /order/check/
class OrderCheckView(View):
    """查看订单支付结果"""
    def post(self, request):
        """查询支付结果"""
        user = request.user

        if not user.is_authenticated():
            return redirect(reverse('user:login'))

        order_id = request.POST.get('order_id')

        if not order_id:
            return JsonResponse({'res': 1, 'errmsg': '未传入订单ID!'})

        try:
            order = OrderInfo.objects.get(
                order_id=order_id,
                user=user,
                pay_method=3,
                order_status=1
            )
        except OrderInfo.DoesNotExist:
            return JsonResponse({'res': 2, 'errmsg': "订单不存在！"})

        app_private_key = open('./apps/order/app_private_key.pem').read()
        alipay_public_key = open('./apps/order/alipay_public_key.pem').read()

        alipay = AliPay(
            appid='2016092900627469',
            app_notify_url=None,
            app_private_key_string=app_private_key,
            alipay_public_key_string=alipay_public_key,
            sign_type="RSA2",
            debug=True
        )

        # 返回的是一个字典
        while True:
            query_response = alipay.api_alipay_trade_query(out_trade_no=order_id)

            code = query_response.get('code')
            if code == '10000' and query_response.get('trade_status') == 'TRADE_SUCCESS':
                # 支付成功
                # 获取支付宝交易号
                # 更新订单的支付状态
                trade_no = query_response.get('trade_no')
                order.trade_no = trade_no
                order.order_status = 4      # 待评价
                order.save()

                return JsonResponse({'res': 4, 'message': '支付成功！'})
            elif code == '40004' or code == '10000' and query_response.get('trade_status') == "WAIT_BUYER_PAY":
                # 等待买家付款
                # 业务处理失败，可能一会就可以成功
                import time
                time.sleep(5)
                continue
            else:
                # 支付出错
                return JsonResponse({'res': 3, 'errmsg': '支付出错！'})


# /order/comment/order_id
class OrderCommentView(View):
    """订单评论"""
    def get(self, request, order_id):
        """显示订单评论"""
        user = request.user

        if not user.is_authenticated():
            return redirect(reverse('user:login'))

        if not order_id:
            return render(request, 'error.html', {'errmsg': '订单ID为空'})

        try:
            order = OrderInfo.objects.get(order_id=order_id, user=user)
        except OrderInfo.DoesNotExist:
            return render(request, 'error.html', {'errmsg': '订单不存在！'})

        order.status_name = OrderInfo.ORDER_STATUS[order.order_status]

        order_goods = OrderGoods.objects.filter(order=order)

        for goods in order_goods:
            amount = goods.price * goods.count
            goods.amount = amount

        order.order_skus = order_goods

        context = {
            'order': order,
        }

        return render(request, 'order_comment.html', context)

    def post(self, request, order_id):
        user = request.user

        if not user.is_authenticated():
            return redirect(reverse('user:login'))

        if not order_id:
            return render(request, 'error.html', {'errmsg': '未传入订单ID！'})

        try:
            order = OrderInfo.objects.get(order_id=order_id, user=user)
        except OrderInfo.DoesNotExist:
            return render(request, 'error.html', {'errmsg': '订单不存在！'})

        total_count = request.POST.get('total_count')
        total_count = int(total_count)

        # 遍历每个商品，获取每个商品的ID，和评论
        for i in range(1, total_count+1):
            goods_id = request.POST.get('sku_{}'.format(i))
            content = request.POST.get('content_{}'.format(i), "")

            try:
                order_goods = OrderGoods.objects.get(order=order, sku_id=goods_id)
            except OrderInfo.DoesNotExist:
                continue

            # 保存订单评论
            order_goods.comment = content
            order_goods.save()

        # 修改订单状态为已完成
        order.order_status = 5
        order.save()

        return redirect(reverse('user:order', kwargs={'page': 1}))
