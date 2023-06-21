from django.conf.urls import url
from login import views


urlpatterns = [
    url(r'^$', views.home_page),
    url(r"^login/$", views.login),
    url(r"^login_handle/$", views.login_handle),
    url(r"^register/$", views.register),
    url(r"^register_handle/$", views.register_handle),
    url(r"^logout/$", views.logout),
    url(r"^retrieve_password/$", views.retrieve_password),
    url(r"^retrieve_handle/$", views.retrieve_handle),
]


