from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'articles', views.ArticleViewSet)
router.register(r'index', views.IndexViewSet)
router.register(r'article_categorys', views.ArticleCategoryViewSet)

urlpatterns = router.urls

urlpatterns += [
    url(r'^article_archive/$', views.ArticleArchiveView.as_view()),
    url(r'^the_latest_article/$', views.the_latest_article),
]