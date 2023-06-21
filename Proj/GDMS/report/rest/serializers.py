from rest_framework import serializers

from report.models import Report


class ReportSerializer(serializers.ModelSerializer):
    subject_name = serializers.CharField(source='subject.subject_name', read_only=True)
    teacher_name = serializers.CharField(source='guide_teacher.name', read_only=True)

    class Meta:
        model = Report
        fields = "__all__"
        extra_kwargs = {
            'submit_time': {'format': "%Y-%m-%d %H:%M:%S"},
            'review_time': {"format": "%Y-%m-%d %H:%M:%S"}
        }
