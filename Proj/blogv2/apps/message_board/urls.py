from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import MessageBoardViewSet


router = DefaultRouter()
router.register(r'message_board', MessageBoardViewSet)

urlpatterns = router.urls
urlpatterns += []