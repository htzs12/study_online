from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator,PageNotAnInteger,EmptyPage
from django.http import HttpResponse
from utils.mixin_utils import LoginRequiredMixin

# Create your views here.

from .models import Course,Lesson,CourseResource

from operation.models import UserCourse,UserProfile,UserFavorite,CourseComments



class CourseListView(View):

    def get(self,request):
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses =Course.objects.all().order_by('-click_nums')[:3]

        sort = request.GET.get('sort','')
        if sort:
            if sort == 'students':
                all_courses = all_courses.order_by('-student')
            elif sort == 'hot':
                all_courses = all_courses.order_by('-fav_nums')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 6, request=request)
        courses = p.page(page)

        return render(request,'course-list.html',{
            'all_courses':courses,
            'hot_courses':hot_courses,
            'sort': sort,
             })


class CourseDetailView(View):
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))

        #增加课程点击数
        course.click_nums +=1
        course.save()
        #lesson = course.lesson_set.all().count()

        #user_courses = course.usercourse_set.all()[:5]

        has_fav_course = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True

        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id,fav_type=2):
                has_fav_org = True

        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[1:2]
        else:
            relate_courses = []

        return render(request,'course-detail.html',{
            'course':course,
            #'lesson':lesson,
            #'user_courses':user_courses,
            'relate_courses':relate_courses,
            'has_fav_course':has_fav_course,
            'has_fav_org':has_fav_org
        })


class CourseInfoView(LoginRequiredMixin,View):
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))

        #查询用户是否已经关联了该课程
        user_courses = UserCourse.objects.filter(request.user,course=course)
        if not user_courses:



        user_ids = []
        for user_course in user_courses:
            user_ids.append(user_course.user.id)
        #user_ids = [user_couser.user.id for user_course in user_courses]

        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)

        course_ids = []
        for user_course in user_courses:
            course_ids.append(user_course.course.id)
        # course_ids = [user_couser.course.id for user_course in user_courses]

        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]

        all_resources = CourseResource.objects.filter(course=course)
        return render(request,'course-video.html',{
            'course':course,
            'all_resources':all_resources,
            'relate_courses':relate_courses
        })


class CommentsView(LoginRequiredMixin,View):
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        all_resources = CourseResource.objects.filter(course=course)
        all_comments =CourseComments.objects.all()

        return  render(request,'course-comment.html',{
            'course':course,
            'all_resources':all_resources,
            'all_comments':all_comments
        })


class AddCommentsView(View):
    def post(self,request):
        if not request.user.is_authenticated:
            return HttpResponse('{"status":"fail","msg":"用户未登录"}',content_type='application/json')

        course_id = request.POST.get('course_id',0)
        comments = request.POST.get('comments','')

        if int(course_id) > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse('{"status":"success","msg":"评论成功"}',content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加失败"}',content_type='application/json')




