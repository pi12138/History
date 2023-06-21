from rest_framework.routers import DefaultRouter

from request_and_response.api.views import RequestViewSet
from request_and_response.api.views import ResponseViewSet


router = DefaultRouter()

router.register('request', RequestViewSet, basename='api-request')
router.register('response', ResponseViewSet, basename='api-response')
