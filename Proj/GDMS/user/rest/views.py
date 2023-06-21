from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action

from django.contrib.auth.models import User

from user.rest.serializers import TeacherSettingsSerializer, SelectedStudentSerializer
from user.models import Teacher, Student, Administrator
from subject.models import TaskBook, Subject
from report.models import Report
from design.models import GraduationDesign, GraduationThesis
from user.helpers import get_role
from announcement.rest.paginations import CustomPageiantion
from import_data.helpers import handle_excel_info


class TeacherSettingsViewSet(ViewSet):
    """
    教师设置
    """
    def list(self, request):
        teacher = request.user.teacher
        ser = TeacherSettingsSerializer(instance=teacher)
        return Response(ser.data)

    def update(self, request, pk=None):
        tea = Teacher.objects.filter(id=pk)
        if not tea.exists():
            return Response("该用户不存在", status=400)

        tea = tea[0]
        data = request.data
        user = request.user

        ser = TeacherSettingsSerializer(instance=tea, data=data)
        if not ser.is_valid():
            return Response("传入数据不合法！", status=400)

        user.email = data.get('email', None)
        user.save()
        ser.save()

        return Response(ser.data)


class StudentInfoViewSet(ViewSet):
    """
    学生功能： 学生信息
    """

    @action(detail=False)
    def related_info(self, request):
        """
        与学生相关的一些信息： 课题ID， 任务书ID, 开题报告ID
        """
        user = request.user.student

        subject = None
        task_book = None
        report = None
        design = None
        thesis = None
        if hasattr(user, 'select_student'):
            subject = user.select_student

        if subject:
            subject_id = subject.id

            query_set = TaskBook.objects.filter(subject_id=subject_id, review_result=1)
            task_book = query_set[0] if query_set.exists() else None

            query_set = Report.objects.filter(subject_id=subject_id)
            report = query_set[0] if query_set.exists() else None

            query_set = GraduationDesign.objects.filter(subject_id=subject_id)
            design = query_set[0] if query_set.exists() else None

            query_set = GraduationThesis.objects.filter(subject_id=subject_id)
            thesis = query_set[0] if query_set.exists() else None

        res = {
            'subject_id': subject.id if subject else None,
            'subject_name': subject.subject_name if subject else None,
            'task_book_id': task_book.id if task_book else None,
            'report_id': report.id if report else None,
            'design_id': design.id if design else None,
            'thesis_id': thesis.id if thesis else None,
        }

        return Response(res)


class UserInfoViewSet(ViewSet):
    """
    用户信息
    """

    def list(self, request):
        user = request.user

        role_str, role_obj = get_role(auth_user=user)

        if role_str == 'student':
            return self.student_info(role_obj)
        elif role_str == 'teacher':
            return self.teacher_info(role_obj)
        elif role_str == 'administrator':
            return Response({'role': 'administrator'})

    def create(self, request):
        """管理员功能--添加用户"""
        if not hasattr(request.user, 'administrator'):
            return Response({'error': '必须是管理员用户操作'}, status=400)

        role = request.data.get('role', "")
        role_dict = {
            'admin': self.handle_admin_info,
            'student': self.handle_student_info,
            'teacher': self.handle_teacher_info
        }

        if not role:
            return Response({'error': '未传入用户身份'}, status=400)

        return role_dict[role](request)

    def student_info(self, role):
        res_data = {
            'role': 'student',
            'user_id': role.account_id,
            'student_id': role.id,
            'student_name': role.name,
            'guide_teacher_id': 0,
            'guide_teacher_name': "",
            'guide_teacher_user_id': 0
        }

        if hasattr(role, 'select_student'):
            teacher = role.select_student.questioner
            res_data['guide_teacher_id'] = teacher.id
            res_data['guide_teacher_name'] = teacher.name
            res_data['guide_teacher_user_id'] = teacher.account_id

        return Response(res_data)

    def teacher_info(self, role):
        res_data = {
            'role': 'teacher',
            'user_id': role.account_id,
            'teacher_id': role.id,
            'teacher_name': role.name,
            'guided_students': None
        }

        query_set = role.subject_set.filter(select_student__isnull=False).select_related('select_student')
        students = list()
        for i in query_set:
            student_info = {
                'student_id': i.select_student_id,
                'student_name': i.select_student.name,
                'student_user_id': i.select_student.account_id
            }
            students.append(student_info)

        if len(students) > 0:
            res_data['guided_students'] = students

        return Response(res_data)

    def handle_admin_info(self, request):
        faculty = request.user.administrator.faculty_id
        data = request.data
        username = data.get('username', "")
        password = data.get('password', '')
        name = data.get('name')

        if not all([faculty, username, password]):
            return Response({'error': '用户信息不全'}, status=400)

        user = User.objects.create_user(username=username, password=password)

        try:
            admin = Administrator.objects.create(faculty_id=faculty, account_id=user.id, name=name)
        except Exception as e:
            return Response({'error': e}, status=400)

        return Response({'data': '新建管理员用户{}成功'.format(admin.id)})

    def handle_student_info(self, request):
        data = request.data
        username = data.get('username', "")
        password = data.get('password', '')
        name = data.get('name', '')
        gender = data.get('gender', '')
        klass = data.get('klass', '')
        direction = data.get('direction', '')
        profession = data.get('profession', '')
        faculty = request.user.administrator.faculty_id
        phone = data.get('phone', '')
        qq = data.get('qq', '')

        if not all([name, phone, qq, faculty, username, password]):
            return Response({'error': "用户信息不全"}, status=400)

        user = User.objects.create_user(username=username, password=password)

        try:
            student = Student.objects.create(name=name, gender=gender, klass_id=klass,
                                             diretcion_id=direction, profession_id=profession,
                                             faculty_id=faculty, phone=phone, qq=qq, account_id=user.id)
        except Exception as e:
            return Response({'error': e})

        return Response({'data': '新建学生{}成功'.format(student.id)})
    
    def handle_teacher_info(self, request):
        data = request.data
        username = data.get('username', '')
        password = data.get('password', '')
        name = data.get('name', '')
        gender = data.get('gender', '')
        education = data.get('education', '')
        teacher_title = data.get('teacher_title', '')
        phone = data.get('phone', '')
        qq = data.get('qq', '')
        office = data.get('office', '')
        faculty = request.user.administrator.faculty_id

        if not all([username, password, name, phone, qq, faculty]):
            return Response({'error': "用户信息不全"}, status=400)

        user = User.objects.create_user(username=username, password=password)

        try:
            teacher = Teacher.objects.create(name=name, gender=gender, education=education,
                                             teacher_title=teacher_title, phone=phone, office_id=office,
                                             faculty_id=faculty, account_id=user.id, qq=qq)
        except Exception as e:
            return Response({'error': e}, status=400)

        return Response({'data': '新建教师用户{}成功'.format(teacher.id)})

    @action(methods=['POST'], detail=False)
    def import_user(self, request):
        """批量导入系统用户"""
        query_dict = request.data
        user_type = query_dict.get('type')
        file = query_dict.get('file')

        type_dict = {
            'admin': self.handle_admin_file,
            'teacher': self.handle_teacher_file,
            'student': self.handle_student_file,
        }

        return type_dict[user_type](request, file)

    def handle_admin_file(self, request, file):
        file_data = file.read()
        data_list = handle_excel_info(file_data)
        faculty = request.user.administrator.faculty_id

        i = 1
        error_list = list()
        success_list = list()
        print(data_list)
        for data in data_list[1:]:
            try:
                user = User.objects.create_user(username=data[0], password=data[1])
                Administrator.objects.create(faculty_id=faculty, account_id=user.id, name=data[2])
                success_list.append({'index': i, 'username': user.username})
            except Exception as e:
                error_list.append({'index': i, 'error': str(e)})

        res = {
            'success': success_list,
            'error': error_list
        }
        return Response(res)

    def handle_teacher_file(self, request, file):
        file_data = file.read()
        data_list = handle_excel_info(file_data)
        faculty = request.user.administrator.faculty_id

        i = 1
        error_list = list()
        success_list = list()
        print(data_list)
        for data in data_list[1:]:
            try:
                user = User.objects.create_user(username=data[0], password=data[1])
                Teacher.objects.create(faculty_id=faculty, account_id=user.id, name=data[2], phone=data[3], qq=data[4])
                success_list.append({'index': i, 'username': user.username})
            except Exception as e:
                error_list.append({'index': i, 'error': str(e)})

        res = {
            'success': success_list,
            'error': error_list
        }
        return Response(res)

    def handle_student_file(self, request, file):
        file_data = file.read()
        data_list = handle_excel_info(file_data)
        faculty = request.user.administrator.faculty_id

        i = 1
        error_list = list()
        success_list = list()
        print(data_list)
        for data in data_list[1:]:
            try:
                user = User.objects.create_user(username=data[0], password=data[1])
                Student.objects.create(faculty_id=faculty, account_id=user.id, name=data[2], phone=data[3], qq=data[4])
                success_list.append({'index': i, 'username': user.username})
            except Exception as e:
                error_list.append({'index': i, 'error': str(e)})

        res = {
            'success': success_list,
            'error': error_list
        }
        return Response(res)

    @action(methods=['POST'], detail=False)
    def import_score(self, request):
        file = request.data.get('file')
        file_data = file.read()
        data_list = handle_excel_info(file_data)

        success_list = list()
        error_list = list()
        for data in data_list[1:]:
            try:
                thesis = GraduationThesis.objects.get(subject_id=data[0])
                thesis.score = data[1]
                thesis.save()
                success_list.append(data[0])
            except Exception as e:
                error_list.append({'subject_id': data[0], 'error': str(e)})

        res = {
            'success': success_list,
            'error': error_list
        }

        return Response(res)


class SelectedStudentViewSet(ViewSet):
    """
    已选题学生列表
    """

    def list(self, request):
        query_set = Subject.objects.filter(select_student__isnull=False)
        student_list = [i.select_student for i in query_set]

        page_obj = CustomPageiantion()
        data = page_obj.paginate_queryset(queryset=student_list, request=request, view=self)
        ser = SelectedStudentSerializer(instance=data, many=True)

        return page_obj.get_paginated_response(ser.data)


class MyTaskViewSet(ViewSet):
    """
    我的任务
    """
    def list(self, request):
        role_str, role_obj = get_role(request.user)

        role_dict = {
            'student': self.student_task,
            'teacher': self.teacher_task,
        }

        res = role_dict[role_str](role_obj)

    def student_task(self, user):

        subject = None
        task_book = None
        report = None
        design = None
        thesis = None
        if hasattr(user, 'select_student'):
            subject = user.select_student

        if subject:
            subject_id = subject.id

            query_set = TaskBook.objects.filter(subject_id=subject_id, review_result=1)
            task_book = query_set[0] if query_set.exists() else None

            query_set = Report.objects.filter(subject_id=subject_id)
            report = query_set[0] if query_set.exists() else None

            query_set = GraduationDesign.objects.filter(subject_id=subject_id)
            design = query_set[0] if query_set.exists() else None

            query_set = GraduationThesis.objects.filter(subject_id=subject_id)
            thesis = query_set[0] if query_set.exists() else None

        res = {
            'subject_id': subject.id if subject else None,
            'task_book_id': task_book.id if task_book else None,
            'report_id': report.id if report else None,
            'design_id': design.id if design else None,
            'thesis_id': thesis.id if thesis else None,
        }

        return res
