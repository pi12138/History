from django.conf.urls import url
from .views import ImportData, ImportLocationInfo


urlpatterns = [
    url('^$', ImportData.as_view(), name='data'),
    url(r'^location_data/$', ImportLocationInfo.as_view(), name='import-location-data'),
]