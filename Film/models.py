from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

from users.models import User


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=1)

class Film(models.Model):
    title = models.CharField(max_length=50, verbose_name='Заголовок')
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name='Слаг')
    content = models.CharField(max_length=10000, blank=True, verbose_name='Контент')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, default=None, verbose_name='Фото')
    rating = models.FloatField(max_length=2, verbose_name='Рейтинг', validators=[MinValueValidator(1, message='Минимальная оценка 1'),
                                                                                 MaxValueValidator(10, message='Максимальная оценка 10')])
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT)
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='posts', null=True, default=None)
    likes = models.ManyToManyField(User, related_name='blogpost_like')

    objects = models.Manager()
    published = PublishedManager()

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    def number_of_likes(self):
        return self.likes.count()
class Category(models.Model):
    name = models.CharField(max_length=50, db_index=True, verbose_name='Имя')
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name='Слаг')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class Comments(models.Model):
    films = models.ForeignKey(Film, on_delete=models.CASCADE, verbose_name='Статья', blank=True,
                              null=True, related_name='comments_film')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария', blank=True, null=True)
    create_date = models.DateTimeField(auto_now=True)
    content = models.TextField(verbose_name='Текст комментария')
    