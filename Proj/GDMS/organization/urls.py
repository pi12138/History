from django.conf.urls import url

from .views import get_faculty, get_profession_from_faculty, \
    get_direction_from_profession, get_klass_from_directions, get_office_from_faculty


urlpatterns = [
    url(r'^facultys/$', get_faculty, name="facultys"),
    url(r'^professions/$', get_profession_from_faculty, name="professions"),
    url(r"^directions/$", get_direction_from_profession, name="directions"),
    url(r'^klasses/$', get_klass_from_directions, name="klasses"),
    url(r'^offices/$', get_office_from_faculty, name='offices'),
]