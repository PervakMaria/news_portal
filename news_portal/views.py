from django import forms
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from .models import *


# from django.shortcuts import get_object_or_404
# user = get_object_or_404(User, pk=user_id)


class RegisterForm(forms.Form):
    userlastname = forms.CharField(label=u'Фамилия', required=True, widget=forms.TextInput(attrs={'class': "form-control"}),)
    username = forms.CharField(label=u'Имя', required=True, widget=forms.TextInput(attrs={'class': "form-control"}),)
    email = forms.EmailField(
        label=u'Почта',
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control"}),
        error_messages = {  'required' : "Введите почту",
                            'invalid'  : "Почтовый адрес некорректен"}
    )
    phone = forms.CharField(label=u'Телефон', widget=forms.TextInput(attrs={'class': "form-control"}),)
    password = forms.CharField(label=u'Пароль', widget=forms.PasswordInput(attrs={'class': "form-control"}), required=True)
    password1 = forms.CharField(label=u'Подтвердите пароль', widget=forms.PasswordInput(attrs={'class': "form-control"}), required=True)


    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с такой почтой уже существует")
        return email


    def clean(self):
        password = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')

        if not password == password1:
            raise forms.ValidationError(u'Пароли не совпадают')
        return password


def index(request):
    return render(request, 'news_portal/index.html')


def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(request.POST.get('email', ''), request.POST.get('email', ''), request.POST.get('password', ''))
            user.first_name = request.POST.get('username', '')
            user.last_name = request.POST.get('userlastname', '')
            user.save()
            return HttpResponseRedirect('/accounts/login/')
        # print(request.POST)
    else:
        form = RegisterForm()

    return render(request, 'news_portal/register.html', context={'form': form})


def posts_list(request):
    news = Post.objects.all()
    return render(request, 'news_portal/news.html', context={'news': news})

def post_detail(request, slug):
    single_news = Post.objects.get(slug__iexact=slug)
    return render(request, 'news_portal/news_detail.html', context={"single_news": single_news})

def categories_list(request):
    categories = Tag.objects.all()
    return render(request, 'news_portal/categories_list.html', context={"categories": categories})

def category_detail(request, slug):
    category = Tag.objects.get(slug__iexact=slug)
    return render(request, 'news_portal/category_detail.html', context={"category": category})
