from django.conf.urls import url

from rest_framework.routers import DefaultRouter

from report.rest.views import ReportViewSet


router = DefaultRouter()
router.register('', ReportViewSet, 'api-report')

urlpatterns = router.urls

# urlpatterns = [
#     url(r'^my_subject/$', my_subject, name='my-subject'),
# ] + urlpatterns

