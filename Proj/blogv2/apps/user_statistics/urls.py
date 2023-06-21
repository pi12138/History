from rest_framework.urls import url
from apps.user_statistics import views

urlpatterns = [
    url(r'^interview_count/$', views.interview_count),
    url(r'^article_read_count/$', views.article_read_count),
    url(r'^one_day_visits/$', views.one_day_visits),
    url(r'^today_read_article/$', views.today_read_article),
    url(r'^hot_ip/$', views.hot_ip),
]
