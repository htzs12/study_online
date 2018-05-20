__author__ = 'haoge'
__date__ = '18-5-20 下午3:43'

from django import forms
from .models import UserAsk


class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fileds = ['name','mobile','course_name']