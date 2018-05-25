__author__ = 'haoge'
__date__ = '18-5-16 下午3:09'

from .models import Course,Lesson,Video,CourseResource
import xadmin


class LessonInline():
    model = Lesson
    extra = 0


class CourseAdmin():
    list_display = ['name', 'desc','degree','learn_times','student','fav_nums','image',
                    'click_nums','add_time','get_zj_nums','go_to']
    search_fields = ['name', 'desc','degree','detail','student']
    list_filter = ['name', 'desc','degree','learn_times','student','fav_nums','click_nums','add_time']
    style_fields = {"detail": "ueditor"}

    #model_icon = 'fa fa-user'
    readonly_fields = ['student']
    #exclude = ['student']  不起作用
    #inlines = [LessonInline]不起作用
    list_editable = ['degree','desc'] #编辑

    #refresh_times = [3,5] 自动刷新

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

