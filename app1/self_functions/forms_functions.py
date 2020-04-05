from django import forms
from django.forms import widgets
from django.core.exceptions import ValidationError
from app1.models import UserInfo


class UserForm(forms.Form):
    user = forms.CharField(max_length=32, label="用户名", error_messages={"required": "用户名不为空"},
                           widget=widgets.TextInput(attrs={"class": "form-control"}))
    pwd = forms.CharField(max_length=32, label="密码", error_messages={"required": "密码不为空"},
                          widget=widgets.PasswordInput(attrs={"class": "form-control"}))
    re_pwd = forms.CharField(max_length=32, label="确定密码", error_messages={"required": "确定密码不为空"},
                             widget=widgets.PasswordInput(attrs={"class": "form-control"}))
    email = forms.EmailField(max_length=32, label="邮箱", error_messages={"required": "邮箱不为空"},
                             widget=widgets.TextInput(attrs={"class": "form-control"}))

    def clean_user(self):
        username = self.cleaned_data.get("user")
        user = UserInfo.objects.filter(username=username).first()
        if not user:
            return username
        else:
            raise ValidationError("用户名已经注册")

    def clean(self):
        pwd = self.cleaned_data.get("pwd")
        re_pwd = self.cleaned_data.get("re_pwd")
        if pwd == re_pwd:
            return self.cleaned_data
        else:
            raise ValidationError("两次密码不一致")
