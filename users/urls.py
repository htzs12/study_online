__author__ = 'haoge'
__date__ = '18-5-24 上午5:58'


from django.urls import path,re_path
from .views import UserInfoView

app_name = 'users'


urlpatterns = [
    path('info/',UserInfoView.as_view(),name='user_info'),

]
