from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q

from .models import UserProfile
from .forms import LoginForm, RegisterForm


# Create your views here.


class UserLoginView(View):
    def get(self, request):
        login_form = LoginForm()
        return render(request, 'users/login.html', {"login_form": login_form})

    def post(self, request):
        login_form = LoginForm(request.POST)
        msg = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('../analysis')
            else:
                return render(request, 'login.html', {"msg": "用户名或密码错误！", "login_form": login_form})
        else:
            return render(request, 'login.html', {
                "login_form": login_form,
            })


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return render(request, 'users/login.html', {})


class RegisterView(View):
    def get(self, request):
        if request.session.get('is_login', None):
            return redirect("/analysis/index/")
        register_form = RegisterForm()
        return render(request, 'users/register.html', {"register_form": register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            if password1 != password2:
                message = "两次输入的密码不同！"
                return render(request, 'users/register.html', locals())
            else:
                same_name_user = UserProfile.objects.filter(username=username)
                if same_name_user:
                    message = '用户已经存在，请重新选择用户名！如果您已经拥有账号，可尝试重置密码再登录。'
                    return render(request, 'users/register.html', locals())
                user_profile = UserProfile()
                user_profile.username = username
                user_profile.password = make_password(password1)
                user_profile.is_active = True
                user_profile.save()
                return render(request, 'users/register_info_ok.html', {"message": message})
        else:
            return render(request, 'users/register.html', {"register_form": register_form})



