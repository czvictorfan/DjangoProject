# _*_ coding:utf-8 _*_
__author__ = 'victorfan'
__date__ = '2018/8/14 14:51'
import xadmin

# 导入课程app的各个model模块
from .models import Course, Lesson, Video, CourseResource


# 课程表的管理类
class CourseAdmin(object):

    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums',\
                    'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students', 'fav_nums', 'image', 'click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'image', 'click_nums',\
                   'add_time']


# 章节表的管理类
class LessonAdmin(object):

    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']


# 视频表的管理类
class VideoAdmin(object):

    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


# 视频表的管理类
class CourseResourceAdmin(object):

    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course', 'name', 'download', 'add_time']


# 用xadmin等等register方法将对应的模块和模块的管理类注册
xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)