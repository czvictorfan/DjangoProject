# _*_ coding:utf-8 _*_
from django.shortcuts import render
# 导入基本的View类包
from django.views.generic.base import View
from .models import Course, CourseResource
from operation.models import UserFavorite, CourseComments

# 导入用于分页的插件包
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


class CourseListView(View):
    def get(self, request):
        # 从数据库中，用objects.all()，取出Course的所有实体对象，通过添加时间降序排列
        all_courses = Course.objects.all().order_by("-add_time")

        # 从数据库中，用objects.all()，取出Course的所有实体对象通过点击数降序排列，取出3个
        hot_courses = Course.objects.all().order_by("-click_nums")[:3]

        # 获取前端传过来的"sort"的值，在View进行操作，对课程进行排序
        sort = request.GET.get("sort", "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")
        # 对课程页面进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 传过来all_orgs对象，用Paginator方法对其进行分页
        # 这里的5是 指每一页的数量，文档虽然没写，但是这里要传值
        p = Paginator(all_courses, 3, request=request)

        courses = p.page(page)

        return render(request, 'course-list.html', {
            "all_courses": courses,
            "sort": sort,
            "hot_courses": hot_courses
        })


class CourseDetailView(View):
    '''
    课程详情页
    '''
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 增加课程点击数
        course.click_nums += 1
        course.save()

        # 课程是否收藏，机构收藏
        has_fav_course = False
        has_fav_org = False

        # 判断是否是登录状态
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True

            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        # 取出课程对应的标签
        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:1]
        else:
            relate_courses = []

        return render(request, "course-detail.html", {
            "course": course,
            "relate_courses": relate_courses,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org,
        })


# 课程章节信息
class CourseInfoView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        return render(request, "course-video.html", {
            "course": course,
            "all_resources": all_resources,
        })


# 课程评论页
class CommentsView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.all()
        return render(request, "course-comment.html", {
            "course": course,
            "all_resources": all_resources,
            "all_comments": all_comments,
        })