__author__ = 'haoge'
__date__ = '18-5-20 上午8:03'

from django.urls import path,re_path

from .views import OrgView,AddUserAskView,OrgHomeView,OrgCourseView


app_name = 'organization'

urlpatterns = [
    path('list/',OrgView.as_view(),name='org_list'),
    path('add_ask/',AddUserAskView.as_view(),name='add_ask'),
        # home页面,取纯数字
    re_path('home/(?P<org_id>\d+)/', OrgHomeView.as_view(), name="org_home"),
    re_path('course/(?P<org_id>\d+)/', OrgCourseView.as_view(), name="org_course"),
]