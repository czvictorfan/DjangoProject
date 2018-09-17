# _*_ coding:utf-8 _*_
from random import Random
# 默认django用来发送邮件
from django.core.mail import send_mail
__author__ = 'victorfan'
__date__ = '2018/8/23 18:30'

from users.models import EmailVerifyRecord
from MxOnline.settings import EMAIL_FROM


# 生成邮箱随机验证码的函数
def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


# 向用户发送邮件的函数
def send_register_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = "慕学在线网注册激活链接"
        email_body = "点击下面的链接激活您的账号：http://127.0.0.1:8000/active/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == "forget":
        mail_title = "慕学在线网注册激活链接"
        email_body = "点击下面的链接激活您的账号：http://127.0.0.1:8000/reset/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass