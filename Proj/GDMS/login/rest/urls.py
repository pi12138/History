from django.conf.urls import url

from rest_framework.routers import SimpleRouter

from .views import TestViewSet


router = SimpleRouter()
router.register('test', TestViewSet, basename='test')

urlpatterns = router.urls
