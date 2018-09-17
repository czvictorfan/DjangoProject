# _*_ coding:utf-8 _*_
# pycharm内置组件
from  __future__ import  unicode_literals
from datetime import datetime
# django第三方组件
from django.db import models
from organization.models import CourseOrg, Teacher

# Create your models here.


# 课程表
class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name=u"课程机构", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u"课程名")
    desc = models.CharField(max_length=300, verbose_name=u"课程描述")
    detail = models.TextField(verbose_name=u"课程详情")
    teacher = models.ForeignKey(Teacher, verbose_name=u"讲师", null=True, blank=True)
    degree = models.CharField(verbose_name=u"难度", choices=(("cj", "初级"), ("zj", "中级"), ("gj", "高级")), max_length=2)
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长（分钟数）")
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    fav_nums = models.IntegerField(default=0, verbose_name=u"收藏人数")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name=u"封面图", max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    category = models.CharField(default=u'后端开发', max_length=20, verbose_name=u"课程类别")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    # 用于推荐课程归类
    tag = models.CharField(default='', verbose_name=u"课程标签", max_length=10)
    youneed_know = models.CharField(default='', max_length=300, verbose_name=u"课程须知")
    teacher_tell = models.CharField(default='', max_length=300, verbose_name=u"老师告诉你")

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        # 获取课程章节数
        return self.lesson_set.all().count()

    # 学习这门课程的人数
    def get_learn_users(self):
        return self.usercourse_set.all()[ :5]

    # 获得课程的所有章节
    def get_course_lesson(self):
        return self.lesson_set.all()

    def __str__(self):
        return self.name


# 章节表
class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"章节名")
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    # 获取所有的章节视频信息
    def get_lesson_video(self):
        return self.video_set.all()


# 学习视频表
class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u"章节")
    name = models.CharField(max_length=100, verbose_name=u"视频名")
    url = models.CharField(max_length=200, verbose_name=u"访问地址", default="")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长（分钟数）")

    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 课程资源表
class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u"课程")
    name = models.CharField(max_length=100, verbose_name=u"资源名")
    download = models.FileField(upload_to="course/resource/%Y/%m", verbose_name=u"资源文件", max_length=100 )
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name






