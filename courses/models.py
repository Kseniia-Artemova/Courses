from django.core.exceptions import ValidationError
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
    course = models.ForeignKey(Course,
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True,
                               related_name='lessons',
                               verbose_name='Курс')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Payment(models.Model):

    WAYS_PAY = (
        ('card', 'Картой'),
        ('cash', 'Наличными')
    )

    client = models.EmailField(max_length=250, verbose_name='E-mail')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата платежа')
    amount = models.PositiveIntegerField(verbose_name='Сумма оплаты')
    way_pay = models.CharField(max_length=4, choices=WAYS_PAY, verbose_name='Способ оплаты')

    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True,
                               related_name='clients',
                               verbose_name='Курс')
    lesson = models.ForeignKey(Lesson,
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True,
                               related_name='clients',
                               verbose_name='Урок')

    def __str__(self):
        return f"{self.date}: {self.client} - {self.amount}"

    def clean(self):
        if self.course and self.lesson:
            raise ValidationError('Нужно выбрать что-то одно')
        elif not self.course and not self.lesson:
            raise ValidationError('Нужно заполнить поле Курса или поле Урока')

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'
