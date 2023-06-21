from django.conf.urls import url

from rest_framework.routers import DefaultRouter

from announcement.rest.views import AnnouncementViewSet


router = DefaultRouter()
# router.register('', ReportViewSet, 'api-report')
router.register('', AnnouncementViewSet, 'api-announcement')

urlpatterns = router.urls


