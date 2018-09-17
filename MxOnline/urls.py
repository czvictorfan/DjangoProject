# _*_ encoding:utf-8 _*_
"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
# 导入可以把html文件变成view的TemplateView类
from django.views.generic import TemplateView

import xadmin
# 用于处理静态文件
from django.views.static import serve

# 从app中的user的view中导入类
from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView
# 从app中的organization的view中导入类
from organization.views import OrgView
from MxOnline.settings import MEDIA_ROOT
# 首页配置的时候前面不用加"/"，不能url('^/login/$',而是要url('^login/$',
urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url('^$', TemplateView.as_view(template_name="index.html"), name="index"),
    url('^login/$', LoginView.as_view(), name="login"),
    url('^register/$', RegisterView.as_view(), name="register"),
    url(r'^captcha/', include('captcha.urls')),
    # 把传回的链接，如http://127.0.0.1:8000/active/uYyUk92u188xOiE8，截取active/后面字符串返回给user_active
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name="user_active"),
    url(r'^forget/$', ForgetPwdView.as_view(), name="forget_pwd"),
    # 把忘记密码传回的链接，如http://127.0.0.1:8000/reset/uYyUk92u188xOiE8，截取reset/后面字符串返回给reset_pwd
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name="reset_pwd"),
    url(r'^modify_pwd/$', ModifyPwdView.as_view(), name="modify_pwd"),


    # 设置前端识别到media/路径时的搜索处理路径(配置上传文件的访问处理函数)
    url(r'^media/(?P<path>.*)$', serve, {"document_root":MEDIA_ROOT}),
    # 课程机构首页，通过{% block XXX %}继承base.html实现子模板的生成
    # 课程机构url配置
    url(r'^org/', include('organization.urls', namespace="org")),

    # 课程相关url配置
    url(r'^course/', include('courses.urls', namespace="course")),

]
