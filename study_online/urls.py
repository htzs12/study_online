"""study_online URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
from django.views.generic import TemplateView
from django.views.static import serve
import xadmin
from study_online.settings import MEDIA_ROOT

from users.views import LoginView,RegisterView,ActiveUserView,\
    LogoutView,ForgetPwdView,ResetView,ModifyPwdView,IndexView


urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    #path('', TemplateView.as_view(template_name='index.html'),name='index'),
    path('', IndexView.as_view(),name='index'),
    path('login/', LoginView.as_view(),name='login'),
    path('logout/', LogoutView.as_view(),name='logout'),
    path('register/', RegisterView.as_view(),name='register'),
    path('forget/', ForgetPwdView.as_view(),name='forget_pwd'),
    path('modify_pwd/', ModifyPwdView.as_view(),name='modify_pwd'),

    re_path('active/(?P<active_code>.*)/',ActiveUserView.as_view(),name='user_active'),
    re_path('reset/(?P<active_code>.*)/',ResetView.as_view(),name='reset_pwd'),

    path("org/", include('organization.urls', namespace='org')),
    path("course/", include('courses.urls', namespace='course')),
    path("users/", include('users.urls')),
    path("captcha/", include('captcha.urls')),

    path('ueditor/', include('DjangoUeditor.urls')),

    #处理图片显示的url, 使用Django自带serve, 传入参数告诉它去哪个路径找，我们有配置好的路径MEDIAROOT
    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),
    #re_path('static/(?P<path>.*)', serve, {"document_root": STATIC_ROOT}),
]

# 全局404页面配置
handler404 = 'user.views.page_not_found'
handler500 = 'user.views.page_error'

