from rest_framework import serializers

from announcement.models import Announcement


class AnnouncementSerializer(serializers.ModelSerializer):
    publisher_name = serializers.CharField(source='publisher.name', read_only=True)
    filename = serializers.SerializerMethodField(method_name='get_filename', read_only=True)

    def get_filename(self, obj):
        if obj.publish_file:
            return obj.publish_file.name.split('/')[-1]
        return None

    class Meta:
        model = Announcement
        fields = "__all__"
        extra_kwargs = {
            'publish_file': {'required': False, 'allow_null': True},
            'publish_time': {'format': "%Y-%m-%d %H:%M:%S"}
        }
