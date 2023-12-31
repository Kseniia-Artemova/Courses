# Generated by Django 4.2.4 on 2023-10-10 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_rename_update_subscription_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='price',
            field=models.PositiveIntegerField(default=10000, verbose_name='Цена'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='price',
            field=models.PositiveIntegerField(default=1000, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='way_pay',
            field=models.CharField(choices=[('card', 'Картой'), ('cash', 'Наличными')], default='card', max_length=4, verbose_name='Способ оплаты'),
        ),
    ]
