"""blogv2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.show.urls')),
    path('media/', include('apps.mediafile.urls')),
]

# api
urlpatterns += [
    path('api/comment/', include('apps.comment.urls')),
    path('api/blogv2/', include('apps.article.urls')),
    path('api/message_board/', include('apps.message_board.urls')),
    path('api/user_statistics/', include('apps.user_statistics.urls')),
    path('api/userinfo/', include('apps.userinfo.urls')),
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]