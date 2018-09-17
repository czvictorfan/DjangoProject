# _*_ encoding:utf-8 _*_
# render回页面的基类
from django.shortcuts import render
# 导入view的基类
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse

# 导入课程机构实体
from operation.models import UserFavorite
from .models import CourseOrg, CityDict
from .forms import UserAskForm
from courses.models import Course
# Create your views here.


class OrgView(View):
    # 课程机构列表功能
    def get(self, request):
        # 取出数据库中的课程机构
        all_orgs = CourseOrg.objects.all()
        # 按点击数“降序排列”取出热门的机构，取出3个
        hot_orgs = all_orgs.order_by("-click_nums")[:3]

        # 取出数据库的城市
        all_cities = CityDict.objects.all()


        # 对城市类别进行筛选
        # 取出筛选出来的城市
        city_id = request.GET.get('city', "")
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 对培训机构类别进行筛选
        # 取出筛选出来的培训机构
        category = request.GET.get('ct', "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 获取前端传过来的"sort"的值，在View进行操作
        sort = request.GET.get("sort","")
        if sort:
            if sort == "students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")


        # 对培训机构类别进行筛选

        # 统计取出来的机构数,需要放在偏后面等上面的筛选完之后
        org_nums = all_orgs.count()
        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # 传过来all_orgs对象，用Paginator方法对其进行分页
        # 这里的5是指每一页的数量，文档虽然没写，但是这里要传值
        p = Paginator(all_orgs, 5, request=request)

        orgs = p.page(page)

        return render(request, "org_list.html", {
            "all_orgs": orgs,
            "all_cities": all_cities,
            "org_nums": org_nums,
            "city_id": city_id,
            "category": category,
            "hot_orgs": hot_orgs,
            "sort": sort
        })


# 生成表单提交的ModelForm所带的View,shift+tab向前缩进
class AddUserAskView(View):
    """
        用户添加咨询
    """
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加出错" }', content_type='application/json')


class OrgHomeView(View):
    # 机构首页
    def get(self, request, org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        # 有外键的地方可以用这种方法方向取出所有的course
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:1]
        return render(request, 'org-detail-homepage.html', {
            'all_course': all_courses,
            'all_teacher': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


class OrgCourseView(View):
    # 机构课程列表页
    def get(self, request, org_id):

        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        # 有外键的地方可以用这种方法方向取出所有的course
        all_courses = course_org.course_set.all()

        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


class OrgDescView(View):
    # 机构介绍页
    def get(self, request, org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


class OrgTeacherView(View):
    # 机构课程教师页
    def get(self, request, org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        # 有外键的地方可以用这种方法方向取出所有的course
        all_teachers = course_org.teacher_set.all()

        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


class AddFavView(View):
    # 用户收藏、用户取消收藏
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        if not request.user.is_authenticated():
            # 判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录" }', content_type='application/json')
        # 判断用户记录是否存在
        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            # 如果记录已经存在，则表示用户取消收藏
            exist_records.delete()
            return HttpResponse('{"status":"success", "msg":"收藏" }', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return HttpResponse('{"status":"success", "msg":"已收藏" }', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错" }', content_type='application/json')

