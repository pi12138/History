from django.conf.urls import url
from cart.views import CartAddView, CartInfoView, CartUpdateView, CartDeleteView


urlpatterns = [
    # Examples:
    # url(r'^$', 'dailyfresh.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^add/$', CartAddView.as_view(), name='add'),
    url(r'^show/$', CartInfoView.as_view(), name="show"),
    url(r'^update/$', CartUpdateView.as_view(), name='update'),
    url(r'^delete/$', CartDeleteView.as_view(), name="delete"),
]
