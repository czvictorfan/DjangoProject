# _*_ encoding:utf-8 _*_
from django.shortcuts import render
# 默认验证方法
from django.contrib.auth import authenticate, login
# CustomBackend要使用的
from django.contrib.auth.backends import ModelBackend
# 导入用来做“或”运算用的方法
from django.db.models import Q
# 基于类来做基本的VIEW配置
from django.views.generic.base import View
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm
from .models import UserProfile, EmailVerifyRecord
# 用户相关的函数,生成密码
from django.contrib.auth.hashers import make_password
# 发送邮件
from utils.email_send import send_register_email


# 用函数的方法配置登录的view
# Backend后端的意思
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            # 并集的查询
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


# 传链接的激活码值
class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


# 传链接的忘记密码激活码
class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                # 设置一个email值，传回去前端用于识别是哪一个email用户
                return render(request, "password_reset.html", {"email": email})
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email, "msg": "密码不一致"})
            user = UserProfile.objects.get(email=email)
            # 用默认模块生成密码
            user.password = make_password(pwd1)
            user.save()

            return render(request, "login.html")
        else:
            email = request.POST.get("email", "")
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})


# 注册的View，一般View都需要在功能最后命名“View”
class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        # 报错调试了很久只因为{'register_form': register_form}里面的:写成=，报需要3元素但只有2的错
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        # 这个位置captcha模块，一个captcha_1参数传不过来的错误调试了一晚上，换了前端导入静态参数的格式就可以
        # 前端用这种形式/static/css/reset.css，而不用{static, 'css/reset.css'}
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            # 判断注册邮箱是否已经存在
            if UserProfile.objects.filter(email=user_name):
                # 重新传值，记得把register_form传回来，这样验证码才能继续显示出来
                return render(request, "register.html", {"register_form": register_form, "msg": "用户已经存在"})
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            # 用默认模块生成密码
            user_profile.password = make_password(pass_word)
            user_profile.save()

            send_register_email(user_name, "register")
            # 成功的话返回登录页面
            return render(request, "login.html")
        else:
            return render(request, "register.html", {"register_form": register_form})


# 根据特定的函数调用特定的方法生成登录VIEW，不用像函数调用那样写if request.method == "POST":
class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        # LoginForm(参数里面需要传入字典)，就传入request.POST
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            # 必须写username=user_name, password=pass_word
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                # 内置方法进行登录，只需要传入request和user对象
                if user.is_active:
                    login(request, user)
                    return render(request, "index.html")
                else:
                    return render(request, "login.html", {"msg": "用户未激活"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误"})
        else:
            return render(request, "login.html", {"login_form": login_form})


# 忘记密码的类
class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {"forget_form": forget_form, "msg": "用户已经存在"})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email, "forget")
            return render(request, "send_success.html")
        else:
            return render(request, "forgetpwd.html", {"forget_form": forget_form, "msg": "用户已经存在"})
# 定义函数名字不要和默认函数名称一样
# def user_login(request):
#     if request.method == "POST":
#         user_name = request.POST.get("username", "")
#         pass_word = request.POST.get("password", "")
#         # 必须写username=user_name, password=pass_word
#         user = authenticate(username=user_name, password=pass_word)
#         if user is not None:
#             # 内置方法进行登录，只需要传入request和user对象
#             login(request, user)
#             return render(request, "index.html")
#         else:
#             return render(request, "login.html", {"msg": "用户名或密码错误"})
#     elif request.method == "GET":
#         return render(request, "login.html", {})
