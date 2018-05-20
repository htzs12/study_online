__author__ = 'haoge'
__date__ = '18-5-20 上午8:03'

from django.urls import path,re_path

from .views import OrgView


app_name = 'organization'

urlpatterns = [
    path('list/',OrgView.as_view(),name='org_list')

]