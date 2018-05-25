__author__ = 'haoge'
__date__ = '18-5-24 上午5:58'


from django.urls import path,re_path
from .views import UserInfoView,UploadImageView,UpdatePwdView,UpdateEmailView,\
    MyCourseView,MyFavOrgView,MyFavTeacherView,MyFavCourseView,MyMessageView
from django.views.decorators.csrf import csrf_exempt

app_name = 'users'


urlpatterns = [
    path('info/',UserInfoView.as_view(),name='user_info'),
    path('image/upload/',UploadImageView.as_view(),name='image_upload'),

    #个人中心修改密码 并解决ajax跨域问题
    #path('update/pwd/',csrf_exempt(UpdatePwdView.as_view()),name='update_pwd'),

    path('update/pwd/',UpdatePwdView.as_view(),name='update_pwd'),
    path('sendemail_code/pwd/',UpdatePwdView.as_view(),name='sendemail_code'),
    path('update_email/', UpdateEmailView.as_view(), name="update_email"),
    path('mycourse/', MyCourseView.as_view(), name="mycourse"),
    path('myfav/org/', MyFavOrgView.as_view(), name="myfav_org"),
    path('myfav/teacher/', MyFavTeacherView.as_view(), name="myfav_teacher"),
    path('myfav/course/', MyFavCourseView.as_view(), name="myfav_course"),
    path('mymessage/', MyMessageView.as_view(), name="mymessage"),
]
