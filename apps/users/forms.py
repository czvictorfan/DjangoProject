# _*_ coding:utf-8 _*_
__author__ = 'victorfan'
__date__ = '2018/8/21 15:44'
from django import forms
# 导入用于验证码功能的类
from captcha.fields import CaptchaField


# 主要用来约束表单填入数据的规范
class LoginForm(forms.Form):
    # required=True这个字段不能为空
    username = forms.CharField(required=True)
    # 设置约束，对数据库也是一种减负的操作
    password = forms.CharField(required=True, min_length=5)


# 注册表单的规范类
class RegisterForm(forms.Form):
    # 默认已经在后台做了Email验证
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    # 验证码模块接口
    captcha = CaptchaField(error_messages={"invalid" : "验证码输入错误"})


# 忘记密码的表单规范类
class ForgetForm(forms.Form):
    # 默认已经在后台做了Email验证
    email = forms.EmailField(required=True)
    # 验证码模块接口
    captcha = CaptchaField(error_messages={"invalid" : "验证码输入错误"})


# 密码修改表单的规范类
class ModifyPwdForm(forms.Form):
    # 老密码
    password1 = forms.CharField(required=True, min_length=5)
    # 新密码
    password2 = forms.CharField(required=True, min_length=5)
