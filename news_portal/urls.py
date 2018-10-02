from django.urls import path, include
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('', index, name="index"),
    path('register/', register_user, name="register_url"),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]
