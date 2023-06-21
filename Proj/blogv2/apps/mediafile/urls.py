from django.conf.urls import url
from .views import load_static_file

urlpatterns = [
    url(r'(?P<path>.*)/(?P<file>.*)', load_static_file),
]