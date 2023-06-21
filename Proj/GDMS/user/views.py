from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from user.helpers import get_role
from user.mixins import LoginRequiredMixin
from organization.models import Faculty

import json


class StudentUserSettingsView(LoginRequiredMixin, View):
    """
    学生用户个人设置
    """
    def get(self, request):
        role_str, role_obj = get_role(request.user)
        
        student = self.get_student_info(request.user, role_obj)
        context = {
            "student": student,
        }
        return render(request, 'student_settings.html', context)

    def post(self, request):
        info = self.get_info(request.POST)
    
        if not all(info):
            context = {
                "error_msg": "信息不全，请填写完毕再次提交！",
                "student": self.get_student_info(request.user, request.user.student)
            }
            return render(request, 'student_settings.html', context)

        user = User.objects.get(username=info[0])
        role_obj = user.student
        user.email = info[5]
        role_obj.name = info[1]
        role_obj.phone = info[2]
        role_obj.gender = int(info[3])
        role_obj.qq = info[4]
        role_obj.faculty_id = info[6]
        role_obj.profession_id = info[7]
        role_obj.diretcion_id = info[8]
        role_obj.klass_id = info[9]
        user.save()
        role_obj.save()

        context = {
            "student": self.get_student_info(user, role_obj)
        }

        return render(request, 'student_settings.html', context)
        

    def get_student_info(self, user, role):
        """
        获取学生信息，返回一个学生信息字典
        user: auth_user 账号
        role: 账号角色对象，即student实例
        """
        student = {}
        student['username'] = user.username
        student['name']  = role.name
        student['phone'] = role.phone
        student['gender'] = role.gender
        student['qq'] = role.qq
        student['email'] = user.email
        student['faculty'] = role.faculty.id if role.faculty else 0
        student['profession'] = role.profession.id if role.profession else 0
        student['direction'] = role.diretcion.id if role.diretcion else 0
        student['klass'] = role.klass.id if role.klass else 0

        # print(student)
        return student

    def get_info(self, post):
        username = post.get('username')
        name = post.get('name')
        phone = post.get('phone')
        gender = post.get('gender')
        qq = post.get('qq')
        email = post.get('email')
        faculty = int(post.get('faculty'))
        profession = int(post.get('profession'))
        direction = int(post.get('direction'))
        klass = int(post.get('klass'))

        info = [username, name, phone, gender, qq, email, faculty, profession, direction, klass]
        print(info)

        return info


@csrf_exempt
def change_password(request):
    body = request.body.decode()
    post = json.loads(body)

    old_password = post.get('old_password')
    new_password1 = post.get('new_password1')
    new_password2 = post.get("new_password2")
    user = request.user

    if not user.check_password(old_password):
        return JsonResponse("密码错误！", status=400, safe=False)

    if old_password == new_password1:
        return JsonResponse("新旧密码一样！", status=400, safe=False)

    if new_password1 != new_password2:
        return JsonResponse("新密码不一致", status=400, safe=False)

    user.set_password(new_password1)
    user.save()

    return JsonResponse("修改密码成功！", status=200, safe=False)


class AdminSettings(LoginRequiredMixin, View):
    """
    管理员设置
    """

    def get(self, request):
        admin = request.user.administrator
        context = {
            'faculty': admin.faculty,
            'name': admin.name,
            'faculty_id': admin.faculty_id
        }
        return render(request, 'admin_settings.html', context)


class TeacherSettings(LoginRequiredMixin, View):
    """
    教师设置
    """

    def get(self, request):
        return render(request, 'teacher_settings.html')


def student_subject(request):
    """
    学生申请课题和已经确定的课题
    """
    user = request.user.student

    if hasattr(user, 'apply_students'):
        pass


class StudentHomeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'student_home.html')


class TeacherHomeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'teacher_home.html')


class AdminHomeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'administrator_home.html')
