from django.shortcuts import render

def index(request):
    return render(request, 'news_portal/index.html')
