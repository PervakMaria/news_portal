from django.db import models
from django.shortcuts import reverse
# from django.utils.text import slugify
from time import time
import re


def slugify(s):
    pattern = r'[^\w+]'
    vocabulary = {'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'e',
      'ж':'zh','з':'z','и':'i','й':'i','к':'k','л':'l','м':'m','н':'n',
      'о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f','х':'h',
      'ц':'c','ч':'cz','ш':'sh','щ':'scz','ъ':'','ы':'y','ь':'','э':'e',
      'ю':'u','я':'ja', 'А':'a','Б':'b','В':'v','Г':'g','Д':'d','Е':'e','Ё':'e',
      'Ж':'zh','З':'z','И':'i','Й':'i','К':'k','Л':'l','М':'m','Н':'n',
      'О':'o','П':'p','Р':'r','С':'s','Т':'t','У':'u','Ф':'Х','х':'h',
      'Ц':'c','Ч':'cz','Ш':'sh','Щ':'scz','Ъ':'','Ы':'y','Ь':'','Э':'e',
      'Ю':'u','Я':'ja',',':'','?':'',' ':'_','~':'','!':'','@':'','#':'',
      '$':'','%':'','^':'','&':'','*':'','(':'',')':'','-':'','=':'','+':'',
      ':':'',';':'','<':'','>':'','\'':'','"':'','\\':'','/':'','№':'',
      '[':'',']':'','{':'','}':'','ґ':'','ї':'', 'є':'','Ґ':'g','Ї':'i','Є':'e'}
    for key in vocabulary:
        s = s.replace(key, vocabulary[key])
    return re.sub(pattern, '-', s)

def gen_slug(s):
    new_slug = slugify(s)
    return new_slug + '-' + str(int(time())) # make unique



class Post(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    body = models.TextField(blank=True, db_index=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name = 'posts')
    date_pub = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('news_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('news_update_url', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.title)


class Tag(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True)

    def get_absolute_url(self):
        return reverse('category_detail_url', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('category_update_url', kwargs={'slug': self.slug})

    def __str__(self):
        return '{}'.format(self.title)
