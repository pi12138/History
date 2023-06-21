from django.conf.urls import url
from user import views


urlpatterns = [
    url(r'^user_info/$', views.user_info),
    url(r"^inquire/$", views.inquire),
    url(r"^books_list/(?P<page_index>[0-9]*)$", views.books_list),
    url(r"^search_books/$", views.search_books),
    url(r"^borrowing_books/$", views.borrowing_books),
    url(r"^returning_books/$", views.returning_books),
    url(r"^not_returned_books/$", views.not_returned_books),
    url(r"^alter_user_info/$", views.alter_user_info),
    url(r"^alter_user_info_handle/$", views.alter_user_info_handle),
    url(r"^delete_user_info/$", views.delete_user_info),
    url(r"^delete_user_info_handle/$", views.delete_user_info_handle),
]
