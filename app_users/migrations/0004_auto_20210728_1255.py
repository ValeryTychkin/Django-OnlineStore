# Generated by Django 2.2 on 2021-07-28 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0003_auto_20210724_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='amount',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='shoppinghistory',
            name='amount',
            field=models.PositiveIntegerField(default=1, verbose_name='amount'),
        ),
    ]