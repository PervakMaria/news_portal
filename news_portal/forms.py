from django import forms
from django.core.exceptions import ValidationError

from .models import *

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
