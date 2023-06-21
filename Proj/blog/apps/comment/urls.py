from django.conf.urls import url
from apps.comment.views import CommentSubmitView


urlpatterns = [
    url(r'^submit/$', CommentSubmitView.as_view(), name='submit'),
]
