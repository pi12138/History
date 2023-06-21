from django.conf.urls import url
from apps.feedback.views import FeedBackListView, FeedBackAddView


urlpatterns = [
    url(r'^list/$', FeedBackListView.as_view(), name='list'),
    url(r'^add/$', FeedBackAddView.as_view(), name='add'),
]