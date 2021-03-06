__author__ = 'hao'
__time__ = '18-5-17 下午3:29'


from random import Random
from django.core.mail import send_mail
from study_online.settings import EMAIL_FROM

from users.models import EmailVerifyRecord


#生成随机字符串

def random_str(random_length=8):
    str = ''

    #生成字符串的可选字符串

    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str += chars[random.randint(0,length)]
    return str

#发送注册邮件

def send_register_email(email,send_type='register'):
    email_record =EmailVerifyRecord()
    if send_type == 'update_email':
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    #定义邮件内容
    email_title = ''
    email_body = ''

    if send_type == 'register':
        email_title ='我是你浩哥 注册激活链接'
        email_body = "请点击下面的链接激活你的账号：http://127.0.0.1:8000/active/{0}".format(code)

        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass

    elif send_type == 'forget':
        email_title = '找回密码重置链接'
        email_body = '请点击下面链接修改你的密码:http://127.0.0.1:8000/reset/{0}'.format(code)

        send_status = send_mail(email_body,email_body,EMAIL_FROM,[email])
        if send_status:
            pass

    elif send_type == 'update_email':
        email_title = '邮箱重置验证码链接'
        email_body = '请点击下面链接修改你的邮箱:http://127.0.0.1:8000/reset/{0}'.format(code)

        send_status = send_mail(email_body, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
