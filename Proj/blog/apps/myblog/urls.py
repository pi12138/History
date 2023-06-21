from django.conf.urls import url
from apps.myblog.views import IndexView, ArticleShowView, ArticleSearchView


urlpatterns = [
    url(r'^(?P<index>\d*)$', IndexView.as_view(), name="index"),
    url(r'^article/(?P<article_id>\d+)$', ArticleShowView.as_view(), name="show"),
    url(r'^search/$', ArticleSearchView.as_view(), name='search'),
]
