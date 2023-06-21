from django.conf.urls import url

from rest_framework.routers import DefaultRouter

from design.rest.views import GraduationDesignViewSet, GraduationThesisViewSet, GraduationReplyViewSet


router = DefaultRouter()
# router.register('', ReportViewSet, 'api-report')
router.register('design', GraduationDesignViewSet, 'api-design')
router.register('thesis', GraduationThesisViewSet, 'api-thesis')
router.register('reply', GraduationReplyViewSet, 'api-reply')

urlpatterns = router.urls


