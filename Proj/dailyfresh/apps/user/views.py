from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.core.urlresolvers import reverse
from django.conf import settings
from django.views.generic import View
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.contrib.auth import authenticate, login, logout
from django_redis import get_redis_connection
from django.core.paginator import Paginator

from user.models import User, Address
from goods.models import GoodsSKU
from order.models import OrderInfo, OrderGoods
from celery_tasks.tasks import send_register_email
from utils.mixin import LoginRequiredMixin
import re
# Create your views here.


# /user/register/
class RegisterView(View):
    def get(self, request):
        return render(request, "register.html")

    def post(self, request):
        # 1. 接收数据
        user_name = request.POST.get('user_name')
        pwd = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 2. 数据校验
        # all(iteranle)方法，可当迭代对象对象的所有元素不为0、''、False或者空对象，则返回True，否则返回False
        if not all([user_name, pwd, email]):
            # 2.1 判断数据是否完整
            return render(request, 'register.html', {'errormsg': "您输入的内容不完整！"})

        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            # 2.2 判断邮箱是否正确
            return render(request, 'register.html', {'errormsg': '邮箱格式不正确！'})

        if allow != 'on':
            # 2.3 判断用户是否同意用户协议
            return render(request, 'register.html', {"errormsg": "请同意用户协议！"})

        try:
            # 2.4 判断账户是否已经被注册，
            user = User.objects.get(username=user_name)
        except User.DoesNotExist as e:
            # 账户未被注册
            user = None

        if user:
            return render(request, 'register.html', {'errormsg': '该账户已经被注册！'})

        # 3. 进行注册流程
        user = User.objects.create_user(username=user_name, password=pwd, email=email)
        user.is_active = 0
        user.save()

        # 4. 发送激活邮件
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        token = serializer.dumps(info)
        token = token.decode()

        send_register_email.delay(user_name, email, token)

        return redirect(reverse('goods:index'))


# /user/active/{}
class ActiveView(View):
    """
    账户激活
    """
    def get(self, request, token):
        serializer = Serializer(settings.SECRET_KEY, 3600)
        print(token)
        try:
            # 解密获取数据
            info = serializer.loads(token)
            user_id = info['confirm']

            # 查询用户信息，修改激活项
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()

            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            return HttpResponse("激活码已过期")


# /user/login/
class LoginView(View):
    """
    登录
    """
    def get(self, request):
        """显示登录页面"""
        # 判断是否记住了用户名
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''

        context = {
            'username': username,
            'checked': checked,
        }

        return render(request, "login.html", context)

    def post(self, request):
        """登录校验"""
        # 1. 接收数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')

        # 2. 进行数据校验
        if not all([username, password]):
            return render(request, 'login.html', {'errormsg': '你输入的内容不完整！'})

        # 3. 进行业务处理:登录校验
        # django自带登录校验
        user = authenticate(username=username, password=password)
        if user is not None:
            # 用户名和密码正确
            if user.is_active:
                # is_active 为 1 代表激活， 为 0 代表未激活
                # 记录用户的登录状态
                login(request, user)

                # 获取登录后需要跳转的页面
                # 如果没有，默认跳转到首页
                next_url = request.GET.get("next", reverse('goods:index'))

                response = redirect(next_url)

                remember = request.POST.get('remember')

                if remember == "on":
                    # 记住用户名
                    response.set_cookie('username', username, max_age=7*24*3600)
                else:
                    response.delete_cookie('username')
                return response

            else:
                return render(request, "login.html", {'errormsg': '账户未激活，请前往绑定邮箱激活！'})

        else:
            return render(request, 'login.html', {'errormsg': '用户名或者密码错误！'})


# /user/logout/
class LogoutView(View):
    """注销登录类"""
    def get(self, request):
        # 注销登录，清除session信息
        logout(request)

        # 重定向到首页
        return redirect(reverse('goods:index'))


# /user
class UserInfoView(LoginRequiredMixin, View):
    """用户中心--个人信息类"""
    def get(self, request):

        # 获取用户个人信息
        user = request.user
        address = Address.objects.get_default_address(user)

        # 获取用户历史浏览记录
        # 1). 链接数据库
        con = get_redis_connection('default')
        history_key = "history_{}".format(user.id)

        # 2). 获取用户最新浏览的5个商品的ID
        sku_ids = con.lrange(history_key, 0, 4)

        # 3). 从数据库查询用户浏览的商品的具体信息, 放到列表中，最后传给模板
        goods_list = []
        for sku_id in sku_ids:
            goods = GoodsSKU.objects.get(id=sku_id)
            goods_list.append(goods)

        content = {
            'page': 'info',
            'address': address,
            'goods_list': goods_list,
        }
        # Django 会给request对象添加一个属性request.user
        # 如果用户未登录，user是一个AnonymousUser类的一个实例对象
        # 如果用户已登录，user是一个User类的一个实例
        # User实例的 is_authenticated 属性始终是 True
        # AnonymousUser.is_authenticated这始终是False
        # 这是一种判断用户是否已通过身份验证的方法。
        # 除了自己给模板传递的模板变量 "context" 外，Django框架会把 request.user 也传给模板文件
        return render(request, 'user_center_info.html', content)


# /user/order/page
class UserOrderView(LoginRequiredMixin, View):
    """用户中心--订单类"""
    def get(self, request, page):
        """显示用户订单页"""

        user = request.user

        # - 查询数据
        #   - 订单创建时间
        #   - 订单编号
        #   - 订单支付状态
        #   - 订单商品
        #   - 商品名称，单位，价格，数量,小计

        try:
            order_list = OrderInfo.objects.filter(user=user).order_by('-create_time')
        except Exception as e:
            return HttpResponse('用户不存在！')

        for order in order_list:
            order_goods_list = OrderGoods.objects.filter(order=order)

            for order_goods in order_goods_list:
                amount = order_goods.count * order_goods.price
                order_goods.amount = amount

            order.order_goods_list = order_goods_list
            order.total_price = order.total_price + order.transit_price
            order.status = order.ORDER_STATUS[order.order_status]

        # 分页
        paginator = Paginator(order_list, 2)

        # 判断 页码page是否合法
        try:
            page = int(page)
        except Exception as e:
            page = 1

        if page > paginator.num_pages:
            page = 1

        order_page = paginator.page(page)

        num_pages = paginator.num_pages

        if num_pages < 5:
            pages = range(1, num_pages+1)
        elif page <= 3:
            pages = range(1, 6)
        elif num_pages-page <= 2:
            pages = range(num_pages-4, num_pages+1)
        else:
            pages = range(page-2, page+3)

        content = {
            'page': 'order',
            'order_list': order_page,
            'pages': pages,
        }
        return render(request, 'user_center_order.html', content)


# /user/site/
class UserSiteView(LoginRequiredMixin, View):
    """用户中心--收货地址类"""
    def get(self, request):
        user = request.user

        # try:
        #     address = Address.objects.get(user=user, is_default=True)
        # except Address.DoesNotExist as e:
        #     address = None

        address = Address.objects.get_default_address(user)

        content = {
            'page': 'site',
            'address': address,
        }
        return render(request, 'user_center_site.html', content)

    def post(self, request):
        """保存收货地址"""
        # 1. 接收数据
        receiver = request.POST.get('receiver')
        addr = request.POST.get('addr')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')

        # 2. 校验数据
        if not all([receiver, addr, phone]):
            return render(request, 'user_center_site.html', {"errormsg": '数据不完整！'})

        if not re.match(r'^1[3|4|5|7|8][0-9]{9}$', phone):
            return render(request, 'user_center_site.html', {'errormsg': '手机号不正确！'})

        # 3. 业务处理
        user = request.user

        # try:
        #     address = Address.objects.get(user=user, is_default=True)
        # except Address.DoesNotExist as e:
        #     address = None

        # 自定义模型类管理器
        address = Address.objects.get_default_address(user)

        if address:
            is_default = False
        else:
            is_default = True

        Address.objects.create(user=user,
                               receiver=receiver,
                               addr=addr,
                               zip_code=zip_code,
                               phone=phone,
                               is_default=is_default)

        # 4. 返回应答
        return redirect(reverse('user:site'))
