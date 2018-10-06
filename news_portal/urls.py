from django.urls import path, include
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('news/', posts_list, name="news"),
    path('news/create/', PostCreate.as_view(), name="news_create_url"),
    path('news/<str:slug>/', post_detail, name="news_detail_url"),
    path('categories/', categories_list, name="categories_list_url"),
    path('categories/create/', CategoryCreate.as_view(), name="category_create_url"),
    path('categories/<str:slug>/', category_detail, name="category_detail_url"),
    path('categories/<str:slug>/update/', CategoryUpdate.as_view(), name="category_update_url"),
    path('register/', register_user, name="register_url"),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]
