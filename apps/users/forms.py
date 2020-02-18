from django.forms import ModelForm
from django import forms

from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label="用户名",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        required=True,
        min_length=8,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="密码"
    )


class RegisterForm(forms.Form):
    username = forms.CharField(label="用户名", min_length=6, max_length=18, help_text="6~18个字符，可使用字母、数字、下划线。", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(required=True, min_length=8, max_length=256, label="密码", widget=forms.PasswordInput(attrs={'class': 'form-control'}), help_text="为保证安全，密码长度请大于8个字符，并同时包含字母与数字")
    password2 = forms.CharField(required=True, min_length=8, max_length=256, label="重复密码", widget=forms.PasswordInput(attrs={'class': 'form-control'}))



