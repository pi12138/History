from django.conf.urls import url

from rest_framework.routers import DefaultRouter

from message_board.rest.views import MessageBoardViewSet


router = DefaultRouter()
# router.register('', ReportViewSet, 'api-report')
router.register('', MessageBoardViewSet, 'api-message-board')

urlpatterns = router.urls


