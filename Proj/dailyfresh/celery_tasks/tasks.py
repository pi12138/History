from django.core.mail import send_mail
from django.conf import settings
from django.template import loader
from celery import Celery
import time

# 任务处理者一端需要有django环境
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dailyfresh.settings')
django.setup()

from goods.models import GoodsType, IndexGoodsBanner, IndexPromotionBanner, IndexTypeGoodsBanner
from django_redis import get_redis_connection

# 创建一个Celery类对象实例
# app = Celery('celery_tasks.tasks', broker='redis://:root@127.0.0.1:6379/8')
app = Celery('celery_tasks.tasks', broker='redis://:root@192.168.0.102:6379/8')

@app.task
def send_register_email(username, email, token):
    """
    发送激活邮件
    :return:
    """
    subject = '注册激活'
    msg = ''
    from_email = settings.EMAIL_FROM
    to_email = email
    html_msg = "<h2>{}，你好</h2><p>点击下面链接激活你的账户</p><br><a href='http://127.0.0.1:8000/user/active/{}'>http://127.0.0.1/user/active/{}</a>".format(username, token, token)

    send_mail(subject, msg, from_email, [to_email], html_message=html_msg, fail_silently=False)

    time.sleep(3)


@app.task
def generate_static_index_html():
    """
    生成未登录的静态主页
    :return:
    """
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

    # 组织模板上下文
    context = {
        'types': types,
        'goods_banners': goods_banners,
        'promotion_banners': promotion_banners
    }

    # 使用模板
    # 1. 加载模板文件，返回模板对象
    # 2. 模板渲染
    temp = loader.get_template('static_index.html')
    static_index_html = temp.render(context)

    # 生成首页对应的静态文件
    save_path = os.path.join(settings.BASE_DIR, 'static/index.html')
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write(static_index_html)
