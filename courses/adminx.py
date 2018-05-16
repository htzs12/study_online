__author__ = 'haoge'
__date__ = '18-5-16 下午3:09'

from .models import Course,Lesson,Video,CourseResource
import xadmin


class CourseAdmin():
    list_display = ['name', 'desc','degree','learn_times','student','fav_nums','image','click_nums','add_time']
    search_fields = ['name', 'desc','degree','detail','student']
    list_filter = ['name', 'desc','degree','learn_times','student','fav_nums','click_nums','add_time']


class LessionAdmin():
    list_display = ['course','name', 'add_time']
    search_fields = ['course','name']
    list_filter = ['course__name','name','add_time']


class VideoAdmin():
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin():
    list_display = ['course', 'name', 'download','add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course', 'name', 'download','add_time']


xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(Lesson,LessionAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)

