# Generated by Django 4.2.4 on 2023-10-12 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_remove_lesson_price_remove_lesson_stripe_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='id_stripe_session',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='id платежной сессии'),
        ),
        migrations.AddField(
            model_name='payment',
            name='is_succeed',
            field=models.BooleanField(default=False, verbose_name='Завершенная оплата'),
        ),
    ]
