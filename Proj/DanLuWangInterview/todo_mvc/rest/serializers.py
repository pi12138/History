from rest_framework import serializers

from todo_mvc.models import Task


class TaskSerializer(serializers.ModelSerializer):
    """
    任务序列化类
    """
    class Meta:
        model = Task
        fields = "__all__"
        extra_kwargs = {'title': {'required': False}}
