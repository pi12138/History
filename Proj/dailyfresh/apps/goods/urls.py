from django.conf.urls import url
from apps.goods import views
from goods.views import IndexView, DetailView, ListView


urlpatterns = [
    # Examples:
    # url(r'^$', 'dailyfresh.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^index/$', views.index, name='index'),
    url(r'^index/$', IndexView.as_view(), name='index'),
    url(r'^goods/(?P<goods_id>\d+)$', DetailView.as_view(), name='detail'),
    url(r'^list/(?P<type_id>\d+)/(?P<page>\d+)', ListView.as_view(), name='list'),
]
