from django.conf.urls import url
from help import views

urlpatterns = [
    url(r"^opinion_list/(?P<page_index>[0-9]*)$", views.opinion_list),
    url(r"^write_opinion/$", views.write_opinion),
    url(r"^guide/$", views.guide),
]