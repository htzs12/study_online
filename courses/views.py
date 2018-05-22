from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator,PageNotAnInteger,EmptyPage

# Create your views here.

from .models import Course,Lesson

from operation.models import UserCourse,UserProfile,UserFavorite



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
