from rest_framework import serializers

from design.models import GraduationDesign, GraduationThesis, GraduationReply
from organization.models import Location


class GraduationDesignSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.subject_name', read_only=True)
    filename = serializers.SerializerMethodField(method_name='get_filename', read_only=True)

    def get_filename(self, obj):
        if obj.design:
            filepath = obj.design.name
            return filepath.split('/')[-1]

        return None

    class Meta:
        model = GraduationDesign
        fields = "__all__"
        extra_kwargs = {
            'upload_time': {'format': "%Y-%m-%d %H:%M:%S"},
            'review_time': {'format': "%Y-%m-%d %H:%M:%S"},
        }


class GraduationThesisSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.subject_name', read_only=True)
    filename = serializers.SerializerMethodField(method_name='get_filename', read_only=True)

    def get_filename(self, obj):
        return obj.thesis.name.split('/')[-1] if obj.thesis else None

    class Meta:
        model = GraduationThesis
        fields = "__all__"
        extra_kwargs = {
            'upload_time': {'format': "%Y-%m-%d %H:%M:%S"},
            'review_time': {'format': "%Y-%m-%d %H:%M:%S"},
        }


class LocationSerializer(serializers.ModelSerializer):
    """
    位置信息序列化类
    """
    class Meta:
        model = Location
        fields = "__all__"


class GraduationReplySerializer(serializers.ModelSerializer):
    """
    毕业答辩信息序列化类
    """
    location_info = serializers.SerializerMethodField(method_name='get_location', read_only=True)
    student_info = serializers.SerializerMethodField(method_name='get_student', read_only=True)

    def get_location(self, obj):
        return {
            'location_number': obj.location.location_number,
            'location_desc': obj.location.location_desc
        }

    def get_student(self, obj):
        return {
            'name': obj.student.name
        }

    class Meta:
        model = GraduationReply
        fields = "__all__"