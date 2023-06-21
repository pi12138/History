from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'comments', views.CommentViewSet)
router.register(r'new', views.NewViewSet)

urlpatterns = router.urls   

urlpatterns += [
    url(r'^get_article_info_from_comment/$', views.get_article_info_from_comment),
]