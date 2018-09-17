# _*_ coding:utf-8 _*_
__author__ = 'victorfan'
__date__ = '2018/9/12 8:59'


from django.conf.urls import url, include
# 在本App中导入CourseListView
from .views import CourseListView, CourseDetailView, CourseInfoView, CommentsView


urlpatterns = [
    # 课程列表页
    url(r'^list/$', CourseListView.as_view(), name="course_list"),
    # 课程详情页
    url(r'^detail/(?P<course_id>\d+)$', CourseDetailView.as_view(), name="course_detail"),
    # 课程信息页
    url(r'^info/(?P<course_id>\d+)$', CourseInfoView.as_view(), name="course_info"),
    # 课程评论页
    url(r'^comment/(?P<course_id>\d+)$', CommentsView.as_view(), name="course_comments"),
   ]