from django.shortcuts import render
from LibraryManagementSystem.settings import captach_id, private_key
from .models import UserInfo
from django.http import HttpResponse
import hashlib
# Create your views here.


def home_page(request):
    """主页"""
    user_name = request.session.get('user_account', None)

    if user_name is None:
        return render(request, "login/homepage.html")
    else:

        context = {
            "user_name": user_name,
        }
        return render(request, "login/homepage.html", context)


def login(request):
    """登录页面"""
    return render(request, "login/login.html")


def login_handle(request):
    """登录信息处理"""

    account = request.POST['user_account']
    password = request.POST['user_password']
    password = encrypt_md5(password)

    try:
        user = UserInfo.objects.get(user_account=account)

        if user.user_password == password:
            # return HttpResponse("登录成功")
            request.session['user_account'] = account

            context = {
                'user_name': account,
            }

            return render(request, "login/homepage.html", context)
        else:
            return HttpResponse("密码错误")

    except Exception as e:
        print("e:", e)
        return HttpResponse("该账户不存在！")

    # return render(request, "login/login.html")


def logout(request):
    """注销"""
    request.session.flush()
    return render(request, "login/homepage.html")


def register(request):
    """注册信息"""
    return render(request, "login/register.html")


def register_handle(request):
    """注册信息处理"""

    account = request.POST["user_account"]

    try:
        user = UserInfo.objects.filter(user_account=account)

        if user.exists():
            # 判断查询集中是否有数据，如果有返回True
            return HttpResponse("该账户已存在，请重新注册！")
        else:
            # 如果查询集中不存在数据表示该账户还未被注册
            password = request.POST["user_password"]
            age = request.POST["user_age"]
            sex = request.POST["user_sex"]
            phone = request.POST["user_phone"]

            # 数据入库,保存
            user = UserInfo()

            user.user_account = account
            # user.user_password = password
            user.user_password = encrypt_md5(password)
            user.user_age = age
            user.user_sex = sex
            user.user_phone = phone

            user.save()

            # return HttpResponse("注册成功！")
            return render(request, 'login/register.html', {"result": "注册成功！"})

    except Exception as e:
        return HttpResponse(e)


def retrieve_password(request):
    """重置密码"""
    return render(request, 'login/retrieve_password.html')


def retrieve_handle(request):
    """重置密码处理"""
    account = request.POST.get("account", None)

    if account is None:
        return HttpResponse("请输入账号！")
    else:

        phone = request.POST.get("phone", None)

        if phone is None:
            return HttpResponse("请输入手机号！")

        try:
            user = UserInfo.objects.filter(user_account=account, user_phone=phone)

            if len(user) == 0:
                return HttpResponse("账号或者手机号错误！")
            else:
                password = request.POST.get("user_password", None)
                if password is None:
                    return HttpResponse("新密码不能为空！")
                else:
                    user[0].user_password = encrypt_md5(password)
                    user[0].save()

                    context = {
                        "password": password,
                    }

                    return render(request, 'login/retrieve_password.html', context)

        except Exception as e:
            return HttpResponse("retrieve_handle error:{}".format(e))


def pcgetcaptcha(request):
    """极验验证码"""
    from geetest import GeetestLib
    import random

    user_id = random.randint(1, 100)
    gt = GeetestLib(captach_id, private_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()

    return HttpResponse(response_str)


def encrypt_md5(password):
    """md5加密"""
    md5 = hashlib.md5()
    md5.update("{}password".format(password).encode())

    return md5.hexdigest()
