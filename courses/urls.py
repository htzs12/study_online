__author__ = 'haoge'
__date__ = '18-5-22 下午7:44'

from django.urls import path,re_path,include
from .views import CourseListView,CourseDetailView,CourseInfoView,CommentsView,AddCommentsView

app_name = 'courses'


urlpatterns = [
    path('list/',CourseListView.as_view(),name='course_list'),
    path('detail/?P<course_id>\d+',CourseDetailView.as_view(),name='course_detail'),
    path('info/?P<course_id>\d+',CourseInfoView.as_view(),name='course_info'),
    path('comment/?P<course_id>\d+',CommentsView.as_view(),name='course_comment'),
    path('add_comment/',AddCommentsView.as_view(),name='add_comment'),
]
