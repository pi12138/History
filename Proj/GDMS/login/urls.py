from django.conf.urls import url

from .views import LoginView, LogoutView


urlpatterns = [
    url(r'^$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name="logout")
]