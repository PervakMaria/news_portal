from django import forms
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect


# from django.shortcuts import get_object_or_404
# user = get_object_or_404(User, pk=user_id)


class RegisterForm(forms.Form):
    userlastname = forms.CharField(label=u'Фамилия', required=True)
    username = forms.CharField(label=u'Имя', required=True)
    email = forms.EmailField(label=u'Почта', required=True)
    phone = forms.CharField(label=u'Телефон')
    password = forms.CharField(label=u'Пароль', widget=forms.PasswordInput(), required=True)
    password1 = forms.CharField(label=u'Подтвердите пароль', widget=forms.PasswordInput(), required=True)

    def clean_username(self):
        email = self.cleaned_data.get('email')

        if not User.objects.filter(email=email).exists():
            return self.cleaned_data

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 == password2:
            return self.cleaned_data
        else:
            raise forms.ValidationError(u'Пароли не совпадают')

def index(request):
    return render(request, 'news_portal/index.html')

def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(request.POST.get('email', ''), request.POST.get('email', ''), request.POST.get('password', ''))
            user.first_name = request.POST.get('username', '')
            user.last_name = request.POST.get('userlastname', '')
            # return HttpResponseRedirect('/')

        # print(request.POST.get('userlastname', ''))
        # print(request.POST)

    form = RegisterForm()
    return render(request, 'news_portal/register.html', context={'form': form})
