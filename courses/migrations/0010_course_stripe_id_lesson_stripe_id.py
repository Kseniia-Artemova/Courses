# Generated by Django 4.2.4 on 2023-10-10 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0009_course_price_lesson_price_alter_payment_way_pay'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='stripe_id',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='id продукта на stripe.com'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='stripe_id',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='id продукта на stripe.com'),
        ),
    ]
