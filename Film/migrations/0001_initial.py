# Generated by Django 5.0.1 on 2024-02-23 15:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=50, verbose_name='Имя')),
                ('slug', models.SlugField(unique=True, verbose_name='Слаг')),
            ],
        ),
        migrations.CreateModel(
            name='Film',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Заголовок')),
                ('slug', models.SlugField(unique=True, verbose_name='Слаг')),
                ('content', models.CharField(blank=True, max_length=10000, verbose_name='Контент')),
                ('photo', models.ImageField(blank=True, default=None, upload_to='photos/%Y/%m/%d', verbose_name='Фото')),
                ('rating', models.FloatField(max_length=2, validators=[django.core.validators.MinValueValidator(1, message='Минимальная оценка 1'), django.core.validators.MaxValueValidator(10, message='Максимальная оценка 10')], verbose_name='Рейтинг')),
                ('time_create', models.DateTimeField(auto_now_add=True)),
                ('time_update', models.DateTimeField(auto_now=True)),
                ('is_published', models.BooleanField(default=True)),
            ],
        ),
    ]
