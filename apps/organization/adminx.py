# _*_ coding:utf-8 _*_
__author__ = 'victorfan'
__date__ = '2018/8/14 15:18'
import xadmin

from .models import CityDict, CourseOrg, Teacher


# 城市字典的管理类
class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


# 课程机构的管理类
class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_nums', 'image', 'address', 'city', 'add_time']
    search_fields = ['name', 'desc', 'click_nums', 'image', 'address', 'city']
    list_filter = ['name', 'desc', 'click_nums', 'image', 'address', 'city', 'add_time']


# 教师的管理类
class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums',\
                    'add_time']
    search_fields = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums']
    list_filter = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_nums', 'fav_nums',\
                   'add_time']


# 用xadmin等等register方法将对应的模块和模块的管理类注册
xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)

