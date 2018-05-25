from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.views.generic.base import View
from django.db.models import Q
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from utils.mixin_utils import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

from .models import UserProfile,EmailVerifyRecord
from .forms import LoginForm,RegisterForm,ForgetForm,ModifyPwdForm,UploadImageForm,UserInfoForm
from pure_pagination import Paginator,PageNotAnInteger,EmptyPage
from utils.email_send import send_register_email
from operation.models import UserCourse,UserFavorite,UserMessage
from organization.models import CourseOrg,Teacher
from courses.models import Course
from .models import Banner

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
                    return HttpResponseRedirect(reverse('index'))
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

            #写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = '欢迎注册哦'
            user_message.save()

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

    def post(self,request):
        user_info = UserInfoForm(request.POST,instance=request.user)
        if user_info.is_valid():
            user_info.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info.errors), content_type='application/json')

    #解决跨域问题
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(UserInfoView,self).dispatch(*args, **kwargs)



#更新头像
class UploadImageView(LoginRequiredMixin,View):
    def post(self,request):
        image_form = UploadImageForm(request.POST,request.FILES,instance=request.user)#指定user
        if image_form.is_valid():
            #image = image_form.cleaned_data['image']
            #request.user.image = image
            #request.user.save()
            image_form.save()
            return HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')

#个人中心修改密码
class UpdatePwdView(View):
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1',"")
            pwd2 = request.POST.get('password2',"")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}',content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return HttpResponse('{"status":"success","msg":"修改成功"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors),content_type='application/json')

    #解决跨域问题
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(UpdatePwdView,self).dispatch(*args, **kwargs)

#发送邮箱验证码
class SendEmailCodeView(LoginRequiredMixin,View):
    def get(self,request):
        email = request.GET.get('email','')

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已存在"}', content_type='application/json')
        send_register_email(email,'update_email')
        return HttpResponse('{"status":"success"}', content_type='application/json')

    #解决跨域问题
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(SendEmailCodeView,self).dispatch(*args, **kwargs)

#修改邮箱
class UpdateEmailView(LoginRequiredMixin,View):
    def post(self,request):
        email = request.POST.get('email','')
        code = request.POST.get('code','')

        existed_records = EmailVerifyRecord.objects.filter(email=email,code=code,send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')

    #解决跨域问题
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(UpdateEmailView,self).dispatch(*args, **kwargs)


class MyCourseView(LoginRequiredMixin,View):
    def get(self,request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request,'usercenter-mycourse.html',{
            'user_courses':user_courses
        })


class MyFavOrgView(LoginRequiredMixin,View):
    def get(self,request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user,fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)

        return render(request,'usercenter-fav-org.html',{
            'org_list':org_list
        })


class MyFavTeacherView(LoginRequiredMixin,View):
    def get(self,request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user,fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)

        return render(request,'usercenter-fav-teacher.html',{
            'teacher_list':teacher_list
        })


class MyFavCourseView(LoginRequiredMixin,View):
    def get(self,request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user,fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)

        return render(request,'usercenter-fav-course.html',{
            'course_list':course_list
        })


class MyMessageView(LoginRequiredMixin,View):
    def get(self,request):
        all_messages = UserMessage.objects.filter(user=request.user.id)
        all_unread_messages = UserMessage.objects.filter(user=request.user.id,has_read=False)
        for unread_message in all_unread_messages:
            unread_message.has_read = True
            unread_message.save()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_messages, 2, request=request)
        messages = p.page(page)

        return render(request,'usercenter-message.html',{
            'all_messages':messages
        })


class IndexView(View):
    def get(self,request):
        all_banner = Banner.objects.order_by('index')
        courses = Course.objects.filter(is_banner=False)[:5]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:3]
        return render(request,'index.html',{
            "all_banner":all_banner,
            'courses':courses,
            'banner_courses':banner_courses,
            'course_orgs':course_orgs
        })

#全局404处理函数
def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html',{})
    response.status_code = 404
    return response

#全局500处理函数
def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html',{})
    response.status_code = 500
    return response