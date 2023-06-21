from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'dailyfresh.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'tinymce', include('tinymce.urls')),
    url(r'^user/', include('user.urls', namespace='user')),
    url(r'^order/', include('order.urls', namespace='order')),
    url(r'^cart/', include('cart.urls', namespace='cart')),
    url(r'^', include('goods.urls', namespace='goods')),

    # 全文检索
    url(r'^search', include('haystack.urls')),
]
