from django.core.exceptions import ValidationError
from django.db import models

from users.models import User


class Course(models.Model):
    """Модель для описания курсов"""

    name = models.CharField(max_length=200, verbose_name='Название')
    preview = models.ImageField(null=True, blank=True, upload_to='', verbose_name='Превью')
    description = models.TextField(null=True, blank=True, verbose_name='Описание')

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True,
                             related_name='courses',
                             verbose_name='Пользователь')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    """Модель для описания уроков"""

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
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             null=True,
                             blank=True,
                             related_name='lessons',
                             verbose_name='Пользователь')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'


class Payment(models.Model):
    """Модель для описания платежей за уроки и курсы"""

    WAYS_PAY = (
        ('card', 'Картой'),
        ('cash', 'Наличными')
    )

    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата платежа')
    amount = models.PositiveIntegerField(verbose_name='Сумма оплаты')
    way_pay = models.CharField(max_length=4, choices=WAYS_PAY, verbose_name='Способ оплаты')

    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='payments',
                             verbose_name='Пользователь')
    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True,
                               related_name='payments',
                               verbose_name='Курс')
    lesson = models.ForeignKey(Lesson,
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True,
                               related_name='payments',
                               verbose_name='Урок')

    def __str__(self):
        return f"{self.date}: {self.user} - {self.amount}"

    def clean(self):
        if self.course and self.lesson:
            raise ValidationError('Нужно выбрать что-то одно')
        elif not self.course and not self.lesson:
            raise ValidationError('Нужно заполнить поле Курса или поле Урока')

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'


class Subscription(models.Model):
    """Модель для описания подписки на обновления курса для пользователя"""

    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               related_name='updates',
                               verbose_name='Курс')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='updates',
                             verbose_name='Пользователь')

    def __str__(self):
        return f"{self.user.email} подписан на обновления курса {self.course.name}"

    class Meta:
        unique_together = ('course', 'user')
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

