from django.urls import path, include
from django.conf.urls import url
from .views import *

urlpatterns = [
    path('', index, name="index"),
    url(r'^accounts/', include('django.contrib.auth.urls')),
]
