from django import forms
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
# from django.http import HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required



from .models import *
from .forms import *


def index(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/news')
    else:
        form = LoginForm()

    return render(request, 'news_portal/index.html', context={'form': form})

def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(request.POST.get('email', ''), request.POST.get('email', ''), request.POST.get('password', ''))
            user.first_name = request.POST.get('username', '')
            user.last_name = request.POST.get('userlastname', '')
            user.save()
            logout(request)
            return redirect('index')
        # print(request.POST)
    else:
        form = RegisterForm()

    return render(request, 'news_portal/register.html', context={'form': form})


class PostCreate(View):
    # @permission_required('create_content', login_url="/login/")
    def get(self, request):
        if request.user.is_authenticated and request.user.is_staff:
            form = PostForm()
            return render(request, 'news_portal/news_create.html', context={"form": form})
        else:
            return redirect('index')
    def post(self, request):
        bound_form = PostForm(request.POST)
        if bound_form.is_valid():
            new_post = bound_form.save()
            return redirect(new_post)
        return render(request, 'news_portal/news_create.html', context={"form": bound_form})

class PostUpdate(View):
    def get(self, request, slug):
        if request.user.is_authenticated and request.user.is_staff:
            post = Post.objects.get(slug__iexact=slug)
            bound_form = PostForm(instance=post)
            return render(request, 'news_portal/news_update.html', context={"form": bound_form, 'post': post})
        else:
            return redirect('index')

    def post(self, request, slug):
        post = Post.objects.get(slug__iexact=slug)
        bound_form = PostForm(request.POST, instance=post)

        if bound_form.is_valid():
            new_post = bound_form.save()
            return redirect(new_post)
        return render(request, 'news_portal/news_update.html', context={"form": bound_form, 'post': post})

@login_required
def posts_list(request):
    news = Post.objects.all()
    return render(request, 'news_portal/news.html', context={'news': news})


def post_detail(request, slug):
    if request.user.is_authenticated:
        single_news = Post.objects.get(slug__iexact=slug)
        return render(request, 'news_portal/news_detail.html', context={"single_news": single_news})
    else:
        return redirect('index')

class CategoryCreate(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.is_staff:
            form = CategoryForm()
            return render(request, 'news_portal/category_create.html', context={"form": form})
        else:
            return redirect('index')

    def post(self, request):
        bound_form = CategoryForm(request.POST)

        if bound_form.is_valid():
            new_category = bound_form.save()
            return redirect(new_category)
        return render(request, 'news_portal/category_create.html', context={"form": bound_form})

class CategoryUpdate(View):
    def get(self, request, slug):
        if request.user.is_authenticated and request.user.is_staff:
            category = Tag.objects.get(slug__iexact=slug)
            bound_form = CategoryForm(instance=category)
            return render(request, 'news_portal/category_update.html', context={"form": bound_form, 'category': category})
        else:
            return redirect('index')

    def post(self, request, slug):
        category = Tag.objects.get(slug__iexact=slug)
        bound_form = CategoryForm(request.POST, instance=category)

        if bound_form.is_valid():
            new_category = bound_form.save()
            return redirect(new_category)
        return render(request, 'news_portal/category_update.html', context={"form": bound_form, 'category': category})


def categories_list(request):
    categories = Tag.objects.all()
    return render(request, 'news_portal/categories_list.html', context={"categories": categories})

def category_detail(request, slug):
    category = Tag.objects.get(slug__iexact=slug)
    return render(request, 'news_portal/category_detail.html', context={"category": category})
