from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
from goods.models import GoodsType, GoodsSKU, IndexGoodsBanner, IndexPromotionBanner, IndexTypeGoodsBanner, Goods
from django_redis import get_redis_connection
from order.models import OrderGoods
# Create your views here.


# def index(request):
#     return render(request, 'index.html')


# http://127.0.0.1:8000/index/
class IndexView(View):
    """首页"""
    def get(self, request):
        '''显示首页'''
        # 尝试从缓存中获取数据
        context = cache.get('index_page_data')

        if context is None:
            print('设置缓存')
            # 缓存中没有数据
            # 获取商品的种类信息
            types = GoodsType.objects.all()

            # 获取首页轮播商品信息
            goods_banners = IndexGoodsBanner.objects.all().order_by('index')

            # 获取首页促销活动信息
            promotion_banners = IndexPromotionBanner.objects.all().order_by('index')

            # 获取首页分类商品展示信息
            for type in types:  # GoodsType
                # 获取type种类首页分类商品的图片展示信息
                image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1).order_by('index')
                # 获取type种类首页分类商品的文字展示信息
                title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0).order_by('index')

                # 动态给type增加属性，分别保存首页分类商品的图片展示信息和文字展示信息
                type.image_banners = image_banners
                type.title_banners = title_banners

            context = {'types': types,
                       'goods_banners': goods_banners,
                       'promotion_banners': promotion_banners}
            # 设置缓存
            # key  value timeout
            cache.set('index_page_data', context, 3600)

        # 获取用户购物车中商品的数目
        user = request.user
        cart_count = 0
        if user.is_authenticated():
            # 用户已登录
            conn = get_redis_connection('default')
            cart_key = 'cart_%d' % user.id
            cart_count = conn.hlen(cart_key)

        # 组织模板上下文
        context.update(cart_count=cart_count)

        # 使用模板
        return render(request, 'index.html', context)


# class IndexView(View):
#     def get(self, request):
#         # - 获取页面数据
#         #   - 获取商品的种类信息
#         #   - 获取首页轮播商品信息
#         #   - 获取首页的促销活动信息
#         #   - 获取首页分类商品展示信息
#         #   - 获取用户购物车中商品数目
#         types = GoodsType.objects.all()
#         index_goods_banner = IndexGoodsBanner.objects.all().order_by('index')
#         index_promotion_banner = IndexPromotionBanner.objects.all().order_by('index')
#
#         for type in types:
#             title_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0).order_by('index')
#             image_banners = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1).order_by('index')
#
#             type.title_banners = title_banners
#             type.image_banners = image_banners
#
#         # 购物车物品数目
#         cart_count = 0
#         user = request.user
#         if user.is_authenticated():
#             # 用户已经登录
#             conn = get_redis_connection('default')
#             cart_key = 'cart_{}'.format(user.id)
#             cart_count = conn.hlen(cart_key)
#
#         context = {
#             'types': types,
#             'goods_banners': index_goods_banner,
#             'promotion_banners': index_promotion_banner,
#             'cart_count': cart_count,
#         }
#
#         return render(request, 'index.html', context)


# https://127.0.0.1/goods/goods_id
class DetailView(View):
    """详情页类"""
    def get(self, request, goods_id):
        # - 获取页面数据
        #   - 判断商品是否存在
        #   - 获取商品分类信息
        #   - 获取商品的评论信息
        #   - 获取新品信息
        #   - 获取同种SPU不同规格的商品
        #   - 获取用户购物车中的商品数目

        try:
            goods = GoodsSKU.objects.get(id=goods_id)
        except GoodsSKU.DoesNotExist:
            # 当商品不存在时
            return redirect(reverse('goods:index'))

        types = GoodsType.objects.all()

        comments = OrderGoods.objects.filter(sku=goods).exclude(comment="")

        new_goods = GoodsSKU.objects.filter(type=goods.type).order_by('-create_time')[:2]

        same_goods = GoodsSKU.objects.filter(goods=goods.goods).exclude(id=goods_id)

        user = request.user
        cart_count = 0
        if user.is_authenticated():
            # 用户已登录
            conn = get_redis_connection('default')
            cart_key = "cart_{}".format(user.id)
            cart_count = conn.hlen(cart_key)

            # 添加用户浏览记录
            conn = get_redis_connection('default')
            history_key = 'history_{}'.format(user.id)
            # 1. 先移除列表中的goods_id
            conn.lrem(history_key, 0, goods_id)
            # 2. 将新浏览的goods_id添加到历史浏览记录
            conn.lpush(history_key, goods_id)
            # 设置历史浏览记录只保存5条
            conn.ltrim(history_key, 0, 4)

        context = {
            'goods': goods,
            'types': types,
            'new_goods': new_goods,
            'comments': comments,
            'cart_count': cart_count,
            'same_goods': same_goods,
        }

        return render(request, 'detail.html', context)


# /list/种类ID/页码/排序方式
# /list/种类ID/页码?sort=排序方式（推荐使用）
# /list?type_id=种类ID&page=页码&sort=排序方式
class ListView(View):
    """列表页"""
    def get(self, request, type_id, page):
        """显示列表页"""

        # - 获取页面数据
        #     - 获取种类信息type，判断种类信息是否正确
        #     - 获取所有商品分类信息types
        #     - 获取排序信息sort，
        #     1.sort = default, 按照id的默认顺序排序
        #     2.sort = price, 按照价格排序
        #     3.sort = hot, 按照销量排序
        #     - 获取同类商品goods_list
        #     - 获取新品信息new_goods
        #     - 对数据进行分页
        #     1.获取页码，对页码进行容错处理
        #     2.获取第page页的内容
        #     3.获取第page页的Page实例对象goods_page
        #     - 获取用户购物车商品数目

        try:
            type = GoodsType.objects.get(id=type_id)
        except GoodsType.DoesNotExist:
            # 商品种类不存在
            return redirect(reverse('goods:index'))

        types = GoodsType.objects.all()

        sort = request.GET.get('sort', 'default')
        if sort == 'default':
            # 默认排序
            goods_list = GoodsSKU.objects.filter(type=type).order_by('id')
        elif sort == "price":
            # 按价格排序，从低到高
            goods_list = GoodsSKU.objects.filter(type=type).order_by('price')
        elif sort == "hot":
            # 按销量排序
            goods_list = GoodsSKU.objects.filter(type=type).order_by('sales')
        else:
            goods_list = GoodsSKU.objects.filter(type=type).order_by('id')
            sort = 'default'

        new_goods = GoodsSKU.objects.filter(type=type_id).order_by('-create_time')[:2]

        paginator = Paginator(goods_list, 1)

        try:
            page = int(page)
        except Exception as e:
            page = 1

        if page > paginator.num_pages:
            # 如果url中的页码大于总页码数
            page = 1

        goods_page = paginator.page(page)

        # - 进行页码控制，页面上最多显示5个页码
        # 1.总页数小于5页，页面上显示所有页码
        # 2.如果当前页是前三页，显示1 - 5页
        # 3.如果当前页是后三页，显示后5页，
        # 4.其他情况，显示当前页的前两页，当前页，当前页的后两页

        page_numbers = paginator.num_pages
        if page_numbers < 5:
            page_list = range(1, page_numbers+1)
        elif page <= 3:
            page_list = range(1, 6)
        elif (page_numbers-2) >= 2:
            page_list = range(page_numbers-4, page_numbers+1)
        else:
            page_list = range(page-2, page+3)

        user = request.user
        cart_count = 0
        if user.is_authenticated():
            # 用户已登录
            conn = get_redis_connection('default')
            cart_key = 'cart_{}'.format(user.id)
            cart_count = conn.hlen(cart_key)

        context = {
            'type': type,
            'types': types,
            # 'goods_list': goods_list,
            'new_goods': new_goods,
            'sort': sort,
            'goods_page': goods_page,
            'page_list': page_list,
            'cart_count': cart_count,
        }

        return render(request, 'list.html', context)
