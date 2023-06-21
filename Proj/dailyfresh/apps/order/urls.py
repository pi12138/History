from django.conf.urls import url
from order.views import OrderPlaceView, OrderCommitView, OrderPayView, OrderCheckView, OrderCommentView


urlpatterns = [
    # Examples:
    # url(r'^$', 'dailyfresh.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^place/$', OrderPlaceView.as_view(), name='place'),
    url(r'^commit/$', OrderCommitView.as_view(), name="commit"),
    url(r'^pay/$', OrderPayView.as_view(), name='pay'),
    url(r'^check/$', OrderCheckView.as_view(), name='check'),
    url(r'^comment/(?P<order_id>\d+)$', OrderCommentView.as_view(), name='comment'),
]
