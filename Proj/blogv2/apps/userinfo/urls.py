from django.conf.urls import url

from .views import UserInfoView


urlpatterns = [
    url(r'^userinfo/', UserInfoView.as_view()),
]