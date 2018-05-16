from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

# Create your views here.

from .models import UserProfile


#实现邮箱和用户名都可以登录

class CustomBackend(ModelBackend):
    def authenticate(self,username=None, password=None, **kwargs):
        try:
            user=UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None



def user_login(request):

    if request.method == 'POST':
        user_name = request.POST.get('username','')
        pass_word = request.POST.get('password','')
        user = authenticate(username=user_name,password=pass_word)
        if user is not None:
            login(request,user)
            return render(request,'index.html')
        else:
            return render(request,'login.html',{'msg':'用户名或密码错误!'})

    elif request.method == 'GET':
        return render(request,'login.html',{})

