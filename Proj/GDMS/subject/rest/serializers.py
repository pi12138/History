from rest_framework import serializers

from subject.models import Subject, ApplySubject, TaskBook
from user.models import Student


class SubjectSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='questioner.name', read_only=True)
    teacher_phone = serializers.CharField(source='questioner.phone', read_only=True)
    teacher_qq = serializers.CharField(source='questioner.qq', read_only=True)
    teacher_email = serializers.CharField(source='questioner.account.email', read_only=True)
    office_name = serializers.CharField(source='questioner.office.name', read_only=True)
    student_name = serializers.SerializerMethodField(method_name="get_student")
    review_result = serializers.SerializerMethodField(method_name='get_review_result')
    reviewer_name = serializers.SerializerMethodField(method_name='get_reviewer_name')
    review_result_number = serializers.IntegerField(source='review_result')
    apply_student = serializers.SerializerMethodField(method_name='get_apply_student')

    def get_student(self, obj):
        if not obj.select_student:
            return ""
        return obj.select_student.name

    def get_review_result(self, obj):
        return obj.get_review_result_display()

    def get_reviewer_name(self, obj):
        if not obj.reviewer:
            return ""
        return obj.reviewer.name

    def get_apply_student(self, obj):
        if hasattr(obj, 'applysubject_set'):
            query_set = obj.applysubject_set.order_by('-apply_time')
            if not query_set.exists():
                return None
            else:
                latest_apply = query_set[0]
                return latest_apply.student.name
        else:
            return None

    class Meta:
        model = Subject
        fields = "__all__"
        extra_kwargs = {
            'questioner': {'read_only': True},
            'declare_time': {'format': "%Y-%m-%d %H:%M:%S", 'read_only': True},
            'select_student': {'read_only': True}
        }


class SubjectInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('id', 'subject_name', 'number_of_people')


class ApplySubjectSerializer(serializers.ModelSerializer):
    subject_info = SubjectInfoSerializer(source='subject', read_only=True)
    student_info = serializers.SerializerMethodField(method_name='get_student_info', read_only=True)

    def get_student_info(self, obj):
        if obj.student is None:
            return ""
        else:
            stu = obj.student
            info = {
                'name': stu.name,
                'qq': stu.qq,
                'phone': stu.phone
            }
            return info

    class Meta:
        model = ApplySubject
        fields = "__all__"
        extra_kwargs = {
            'apply_time': {'format': "%Y-%m-%d %H:%M:%S", 'read_only': True},
        }


class SubjectInfoSerializer(serializers.ModelSerializer):
    select_student = serializers.SerializerMethodField(method_name='get_student', read_only=True)
    task_book = serializers.SerializerMethodField(method_name='get_task_book', read_only=True)
    task_book_status = serializers.SerializerMethodField(method_name='get_task_book_status', read_only=True)
    questioner_info = serializers.SerializerMethodField(method_name='get_questioner', read_only=True)
    report = serializers.SerializerMethodField(method_name='get_report', read_only=True)
    design = serializers.SerializerMethodField(method_name='get_design', read_only=True)
    thesis = serializers.SerializerMethodField(method_name='get_thesis', read_only=True)

    def get_student(self, obj):
        if obj.select_student is None:
            return ""
        else:
            stu = obj.select_student
            info = {
                'name': stu.name,
                'qq': stu.qq,
                'phone': stu.phone
            }
            return info

    def get_task_book(self, obj):
        if hasattr(obj, 'task_book'):
            return obj.task_book.id
        else:
            return None

    def get_questioner(self, obj):
        if obj.questioner:
            return {
                'name': obj.questioner.name
            }
        return None

    def get_task_book_status(self, obj):
        if hasattr(obj, 'task_book'):
            return obj.task_book.review_result
        return None

    def get_report(self, obj):
        if hasattr(obj, 'report'):
            report = {
                'id': obj.report.id,
                'review_result': obj.report.review_result
            }
            return report

        return None

    def get_design(self, obj):
        if hasattr(obj, 'graduationdesign'):
            design = {
                'id': obj.graduationdesign.id,
                'review_option': obj.graduationdesign.review_option,
                'review_time': obj.graduationdesign.review_time
            }
            return design
        return None

    def get_thesis(self, obj):
        if hasattr(obj, 'graduationthesis'):
            thesis = {
                'id': obj.graduationthesis.id,
                'review_option': obj.graduationthesis.review_option
            }
            return thesis
        return None

    class Meta:
        model = Subject
        fields = "__all__"
        extra_kwargs = {
            'declare_time': {'format': "%Y-%m-%d %H:%M:%S", 'read_only': True},
            'review_time': {'format': '%Y-%m-%d %H:%M:%S', 'read_only': True}
        }


class TaskBookSerializer(serializers.ModelSerializer):
    """
    任务书序列化类
    """
    subject_info = serializers.SerializerMethodField(method_name='get_subject', read_only=True)
    reviewer_info = serializers.SerializerMethodField(method_name='get_reviewer', read_only=True)

    def get_subject(self, obj):
        if obj.subject:
            return {
                'name': obj.subject.subject_name
            }
        else:
            return None

    def get_reviewer(self, obj):
        if not obj.reviewer:
            return None
        else:
            return {
                'name': obj.reviewer.name
            }

    class Meta:
        model = TaskBook
        fields = '__all__'
        extra_kwargs = {
            'release_time': {'format': "%Y-%m-%d %H:%M:%S"},
            'review_time': {'format': "%Y-%m-%d %H:%M:%S"}
        }
