from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.hello),
    url(r'^index/$', views.index),
    url(r'^article/(?P<pk>\d+)/$', views.article),
    url(r'^search/$', views.search),
    url(r'^archive/$', views.archive),
    url(r'^message_board/$', views.message_board),
    url(r'^user_statistics/$', views.user_statistics),
    url(r'^favicon.ico$', views.favicon),
]
