from django import forms
from django.forms import widgets


class UserInfo(forms.Form):
    user = forms.CharField(max_length=32, label="用户名",
                           widget=widgets.TextInput(attrs={"class": "form-control"}))
    pwd = forms.CharField(max_length=32, label="密码",
                          widget=widgets.PasswordInput(attrs={"class": "form-control"}))
    re_pwd = forms.CharField(max_length=32, label="确定密码",
                             widget=widgets.PasswordInput(attrs={"class": "form-control"}))
    email = forms.EmailField(max_length=32, label="邮箱",
                             widget=widgets.TextInput(attrs={"class": "form-control"}))
