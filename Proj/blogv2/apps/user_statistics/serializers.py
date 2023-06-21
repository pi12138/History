from .models import UserIP, UserInterviewInfo
from rest_framework.serializers import ModelSerializer


class UserIPSerializer(ModelSerializer):
    class Meta:
        model = UserIP
        fields = "__all__"


class UserInterviewInfoSerializer(ModelSerializer):
    class Meta:
        model = UserInterviewInfo
        fields = "__all__"