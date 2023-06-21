from django.shortcuts import render
from rest_framework import views
from rest_framework.response import Response
# Create your views here.

from .serializers import UserInfoSerializer
from .models import UserInfo


class UserInfoView(views.APIView):
    
    def get(self, request):
        queryset = UserInfo.objects.filter(used=1)

        if queryset.exists():
            user = queryset[queryset.count()-1]
        else:
            user = UserInfo()
            user.name = "xxx"
            user.nickname = "xxx"
            user.github = "xxx.com"
            user.email = "xxx@xx.com"
            user.words = "xxx"
            user.avatar = "static/image/2.jpg"
            user.used = 1

        ser = UserInfoSerializer(instance=user, many=False)

        return Response(ser.data)
