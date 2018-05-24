from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.views.generic.base import View
from django.db.models import Q
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from utils.mixin_utils import LoginRequiredMixin

# Create your views here.

from .models import UserProfile,EmailVerifyRecord
from .forms import LoginForm,RegisterForm,ForgetForm,ModifyPwdForm,UploadImageForm
from utils.email_send import send_register_email


#实现邮箱和用户名都可以登录
class CustomBackend(ModelBackend):
    def authenticate(self,username=None, password=None, **kwargs):
        try:
            user=UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


"""
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
"""

#用户登录
class LoginView(View):
    def get(self,request):
        return render(request,'login.html')

    def post(self,request):
        login_form=LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username','')
            pass_word = request.POST.get('password','')
            user = authenticate(username=user_name,password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    return render(request,'index.html')
                else:
                    return render(request,'login.html',{'msg':'用户未激活,请前往邮箱进行激活'})
            else:
                return render(request,'login.html',{'msg':'用户名或密码错误!'})
        else:
            return render(request,'login.html',{'login_form':login_form})


#用户注册
class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request,'register.html',{'register_form':register_form})

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email','')

            if UserProfile.objects.filter(email=user_name):
                return render(request,'register.html',{'register_form':register_form,'msg':'用户名已存在'})

            pass_word = request.POST.get('password','')

            user_profile = UserProfile()

            user_profile.username = user_name
            user_profile.email = user_name

            user_profile.is_active = False

            user_profile.password = make_password(pass_word)
            user_profile.save()

            send_register_email(user_name,'register')

            return render(request,'login.html',{'msg':'注册邮件已发送，请激活以后登录'})
        else:
            return render(request, 'register.html',{'register_form':register_form})

#激活用户
class ActiveUserView(View):
    def get(self,request,active_code):
        all_record = EmailVerifyRecord.objects.filter(code = active_code)
        if all_record:
            for record in all_record:
                email = record.email

                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()

                return render(request,'login.html',{'msg':'激活成功，请登录'})
        else:
            return render(request,'login.html',{'msg':'您的激活链接无效'})

#退出
class LogoutView(View):
    def get(self,request):
        logout(request)
        return HttpResponseRedirect(reverse('index'))


#忘记密码-发送验证码
class ForgetPwdView(View):
    def get(self,request):
        forget_form = ForgetForm()
        return render(request,'forgetpwd.html',{'forget_form':forget_form})

    def post(self,request):
        forget_form = ForgetForm(request.POST)

        if forget_form.is_valid():
            email = request.POST.get('email',)

            user=UserProfile.objects.filter(email=email)
            if len(user) == 0:
                return render(request,'forgetpwd.html',{'forget_form':forget_form,'msg':'用户不存在'})

            send_register_email(email,'forget')
            return render(request,'login.html',{'msg':'重置密码邮件已经发送，请注意查收。。。'})
        else:
            return render(request,'forgetpwd.html',{'forget_form':forget_form})

#重置密码链接
class ResetView(View):
    def get(self,request,active_code):
        all_record = EmailVerifyRecord.objects.filter(code=active_code)

        if all_record:
            for record in all_record:
                email = record.email

                return render(request,'password_reset.html',{'email':email}) #email必须传，才能知道哪个用户修改
        else:
            return render(request,'forgetpwd.html',{'msg':'您的重置密码链接无效，请重新请求'})

#重置密码更改
class ModifyPwdView(View):
    def get(self,request):
        return render(request,'password_reset.html')

    def post(self,request):
        modifypwd_form = ModifyPwdForm(request.POST)
        if modifypwd_form.is_valid():
            pwd1 = request.POST.get('password1','')
            pwd2 = request.POST.get('password2','')
            email = request.POST.get('email','')

            if pwd1 != pwd2:
                return render(request,'password_reset.html',{'email':email,'msg':'密码不一致'})

            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()
            return render(request,'login.html',{'msg':'密码修改成功，请登录哦'})
        else:
            email = request.POST.get('email','')
            return render(request,'password_reset.html',{'email':email,'modifypwd_form':modifypwd_form})


#用户信息
class UserInfoView(LoginRequiredMixin,View):
    def get(self,request):
        return render(request,'usercenter-info.html',{})


class UploadImageView(LoginRequiredMixin,View):
    def post(self,request):
        image_form = UploadImageForm(request.POST,request.FILES,instance=request.user)
        if image_form.is_valid():
            pass
        return HttpResponse('ok')





