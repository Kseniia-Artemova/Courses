from django.db import models


class Course(models.Model):

    name = models.CharField(max_length=200, verbose_name='Название')
    preview = models.ImageField(null=True, blank=True, upload_to='', verbose_name='Превью')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):

    name = models.CharField(max_length=50, verbose_name='Название')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')
    preview = models.ImageField(null=True, blank=True, upload_to='', verbose_name='Превью')
    video = models.URLField(null=True, blank=True, max_length=200, verbose_name='Видео')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
