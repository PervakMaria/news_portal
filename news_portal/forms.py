from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


from .models import *

class LoginForm(forms.Form):
    username = forms.CharField(label='Почта', required=True, widget=forms.TextInput(attrs={'class': "form-control"}),)
    password = forms.CharField(label='Пароль', required=True, widget=forms.PasswordInput(attrs={'class': "form-control"}),)


    def clean_username(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Такого пользователя не существует")
        return self.cleaned_data


class RegisterForm(forms.Form):
    userlastname = forms.CharField(label='Фамилия', required=True, widget=forms.TextInput(attrs={'class': "form-control"}),)
    username = forms.CharField(label='Имя', required=True, widget=forms.TextInput(attrs={'class': "form-control"}),)
    email = forms.EmailField(
        label='Почта',
        required=True,
        widget=forms.TextInput(attrs={'class': "form-control"}),
        error_messages = {  'required' : "Введите почту",
                            'invalid'  : "Почтовый адрес некорректен"}
    )
    # phone = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'class': "form-control"}),)
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': "form-control"}), required=True)
    password1 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput(attrs={'class': "form-control"}), required=True)


    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с такой почтой уже существует")
        return email


    def clean(self):
        password = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')

        if not password == password1:
            raise forms.ValidationError('Пароли не совпадают')
        return password

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['title', 'slug']
        labels = {
            "title": "Заголовок",
            "slug": "Слаг"
        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'})
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()

        if new_slug == 'create':
            raise ValidationError('Недопустимое значение')
        if Tag.objects.filter(slug__iexact=new_slug).count():
            raise ValidationError('Значение поля слаг должно быть уникальным')
        return new_slug

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'body', 'tags']
        labels = {
            "title": "Заголовок",
            "slug": "Слаг (необязательно к заполнению)",
            "body": "Текст новости",
            "tags": "Категории"

        }

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'})
        }

        def clean_slug(self):
            new_slug = self.cleaned_data['slug'].lower()

            if new_slug == 'create':
                raise ValidationError('Недопустимое значение')
            return new_slug



# class CategoryForm(forms.Form):
#     title = forms.CharField(max_length=50, label='Заголовок', widget=forms.TextInput(attrs={'class': "form-control"}),)
#     slug = forms.CharField(max_length=50, label='Слаг', widget=forms.TextInput(attrs={'class': "form-control"}),)
#
#     def clean_slug(self):
#         new_slug = self.cleaned_data['slug'].lower()
#
#         if new_slug == 'create':
#             raise ValidationError('Недопустимое значение')
#         if Tag.objects.filter(slug__iexact=new_slug).count():
#             raise ValidationError('Значение поля слаг должно быть уникальным')
#         return new_slug
#
#     def save(self):
#         new_tag = Tag.objects.create(
#             title = self.cleaned_data['title'],
#             slug = self.cleaned_data['slug']
#         )
#         return new_tag
