from rest_framework import serializers

from message_board.models import MessageBoard
from user.helpers import get_role


class MessageBoardSerializer(serializers.ModelSerializer):
    publisher_info = serializers.SerializerMethodField(method_name='get_publisher_info', read_only=True)
    receiver_info = serializers.SerializerMethodField(method_name='get_receiver_info', read_only=True)
    filename = serializers.SerializerMethodField(method_name='get_filename', read_only=True)

    def get_publisher_info(self, obj):
        role_str, role_obj = get_role(obj.publisher)
        return {'role': role_str, 'name': role_obj.name}

    def get_receiver_info(self, obj):
        role_str, role_obj = get_role(obj.receiver)
        return {'role': role_str, 'name': role_obj.name}

    def get_filename(self, obj):
        if obj.annex:
            return obj.annex.name.split('/')[-1]
        return None

    class Meta:
        model = MessageBoard
        fields = "__all__"
        extra_kwargs = {
            'publish_time': {'format': "%Y-%m-%d %H:%M:%S"},
            'annex': {'required': False, 'allow_null': True},
        }
