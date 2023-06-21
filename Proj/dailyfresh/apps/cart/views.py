from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
from goods.models import GoodsSKU
from utils.mixin import LoginRequiredMixin

from django_redis import get_redis_connection
# Create your views here.


# /cart/add
class CartAddView(View):
    """添加购物车类"""
    def post(self, request):
        user = request.user
        # 验证登录
        if not user.is_authenticated():
            return JsonResponse({'res': 0, 'errmsg': '请先登录！'})

        # 接收数据
        goods_id = request.POST.get('goods_id')
        count = request.POST.get('count')

        print(goods_id, count)
        # 校验数据
        if not all([goods_id, count]):
            return JsonResponse({'res': 1, 'errmsg': '数据不完整！'})

        try:
            count = int(count)
        except Exception as e:
            return JsonResponse({'res': 2, 'errmsg': '商品数目出错！'})

        try:
            goods = GoodsSKU.objects.get(id=goods_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({'res': 3, 'errmsg': '商品不存在！'})

        # 业务处理：添加到购物车
        # - 先判断购物车中是否存在该物品，如果存在就更新数据，不存在就添加数据
        # - 校验商品的库存
        conn = get_redis_connection('default')
        cart_key = 'cart_{}'.format(user.id)
        cart_count = conn.hget(cart_key, goods_id)

        if cart_count:
            # 如果购物车存在该物品记录，则更新数据
            count += int(cart_count)

        if goods.stock < count:
            return JsonResponse({'res': 4, 'errmsg': '商品库存不足！'})

        conn.hset(cart_key, goods_id, count)

        # 计算用户购物车中的条目数
        total_count = conn.hlen(cart_key)

        return JsonResponse({'res': 5, 'total_count': total_count, 'message': '添加成功！'})


# /cart/show/
class CartInfoView(LoginRequiredMixin, View):
    '''购物车'''
    def get(self, request):
        """显示购物车"""
        user = request.user

        conn = get_redis_connection('default')
        cart_key = 'cart_{}'.format(user.id)
        cart_dict = conn.hgetall(cart_key)

        goods_list = []
        total_count = 0
        total_price = 0
        for goods_id, number in cart_dict.items():
            goods = GoodsSKU.objects.get(id=goods_id)
            number = int(number)

            amount = number*goods.price

            goods.number = number
            goods.amount = amount

            total_count += number
            total_price += amount
            goods_list.append(goods)

        context = {
            'total_count': total_count,
            'goods_list': goods_list,
            'total_price': total_price,
        }

        return render(request, 'cart.html', context)


# /cart/update/
class CartUpdateView(View):
    """购物车更新数据"""
    def post(self, request):
        """更新数据"""
        # 判断用户是否登录
        user = request.user
        if not user.is_authenticated():
            return JsonResponse({'res': 0, 'errmsg': '用户未登录！'})

        # 接收数据
        goods_id = request.POST.get('goods_id')
        count = request.POST.get('count')

        # 数据校验
        if not all([goods_id, count]):
            return JsonResponse({'res': 1, 'errmsg': '数据不完整！'})

        try:
            count = int(count)
        except Exception as e:
            return JsonResponse({'res': 2, 'errmsg': '商品数目有问题！'})

        try:
            goods = GoodsSKU.objects.get(id=goods_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({'res': 3, 'errmsg': '商品不存在!'})

        # 业务流程：更新购物车记录
        conn = get_redis_connection('default')
        cart_key = 'cart_{}'.format(user.id)

        # 判断商品库存是否足够
        if goods.stock < count:
            return JsonResponse({'res': 4, 'errmsg': '商品库存不足！'})

        # 购物车更新数据
        conn.hset(cart_key, goods_id, count)

        total_count = 0
        vals = conn.hvals(cart_key)
        for val in vals:
            total_count += int(val)

        return JsonResponse({'res': 5, 'total_count': total_count, 'message': '更新成功！'})


# /cart/delete/
class CartDeleteView(View):
    """购物车删除"""
    def post(self, request):
        """购物车记录删除"""
        user = request.user
        if not user.is_authenticated():
            return JsonResponse({'res': 0, 'errmsg': '用户未登录！'})

        goods_id = request.POST.get('goods_id')

        # 数据校验
        if not goods_id:
            return JsonResponse({'res': 1, 'errmsg': '数据未传入！'})

        try:
            goods = GoodsSKU.objects.get(id=goods_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({"res": 2, 'errmsg': '商品不存在！'})

        # 业务处理：删除购物车记录
        conn = get_redis_connection('default')
        cart_key = "cart_{}".format(user.id)

        # 删除购物车记录
        conn.hdel(cart_key, goods_id)

        # 获取剩下商品的总数
        total_count = 0
        vals = conn.hvals(cart_key)
        for val in vals:
            total_count += int(val)

        return JsonResponse({'res': 3, 'message': '删除记录成功！', 'total_count': total_count})
