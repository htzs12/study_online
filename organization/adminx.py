__author__ = 'haoge'
__date__ = '18-5-16 下午10:10'

from .models import Teacher,CityDict,CourseOrg
import xadmin


class CityDictAdmin():
    list_display = ['name','desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name','desc', 'add_time']


class CourseOrgAdmin():
    list_display = ['city','name', 'desc', 'click_nums','fav_nums','address','image','add_time']
    search_fields = ['city','name','click_nums','fav_nums','address']
    list_filter = ['city','name', 'desc', 'click_nums','fav_nums','address','image','add_time']


class TeacherAdmin():
    list_display = ['org', 'name', 'work_years','work_company','work_positon','points','click_nums','fav_ums','add_time']
    search_fields = ['org', 'name', 'work_years','work_company','work_positon','points']
    list_filter = ['org', 'name', 'work_years','work_company','work_positon','points','click_nums','fav_ums','add_time']


xadmin.site.register(CityDict,CityDictAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)
xadmin.site.register(Teacher,TeacherAdmin)