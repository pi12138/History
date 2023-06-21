from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.urls import reverse
# Create your views here.
from user.helpers import get_role


class LoginView(View):
    """
    登录视图
    """
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get("password")
        next = request.GET.get('next')

        if not all([username, password]):
            return render(request, 'login.html', {'error_msg': "必须填写所有信息！"})
        
        user = authenticate(username=username, password=password)
        if not user:
            return render(request, 'login.html', {'error_msg': "账号或者密码错误！"})
        else:
            login(request, user)

            role_str, role_obj = get_role(user)
            role_dict = {
                "teacher": "user/teacher_settings/",
                "student": "user/student_settings/",
                "administrator": "user/administrator_settings/",
            }

            if not role_str:
                return render(request, 'login.html', {'error_msg': "账户异常！"})
            if not next:
                # return render(request, role_dict[role_str])
                return redirect(role_dict[role_str])
            else:
                return redirect(next)
        

class LogoutView(View):
    """
    登出
    """
    def get(self, request):
        logout(request)

        return redirect(reverse('login:login'))