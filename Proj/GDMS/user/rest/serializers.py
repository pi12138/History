from rest_framework import serializers

from user.models import Teacher, Student


class TeacherSettingsSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='account.email', read_only=True)
    faculty_name = serializers.CharField(source='faculty.name', read_only=True)

    class Meta:
        model = Teacher
        fields = "__all__"
        extra_kwargs = {
            'faculty': {'read_only': True}
        }


class SelectedStudentSerializer(serializers.ModelSerializer):
    subject = serializers.SerializerMethodField(method_name='get_subject', read_only=True)
    message_info = serializers.SerializerMethodField(method_name='get_message', read_only=True)

    def get_subject(self, obj):
        if hasattr(obj, 'select_student'):
            subject = obj.select_student
            return {
                'name': subject.subject_name,
                'id': subject.id,
                'questioner_id': subject.questioner_id,
                'questioner_name': subject.questioner.name
            }
        return None

    def get_message(self, obj):
        user = obj.account
        if hasattr(user, 'message_board_publisher'):
            messages = user.message_board_publisher
            return {
                'count': messages.count()
            }
        return None

    class Meta:
        model = Student
        fields = ('id', 'subject', 'message_info', 'name', 'account')
