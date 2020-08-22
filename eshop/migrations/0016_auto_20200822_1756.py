# Generated by Django 3.0.8 on 2020-08-22 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0015_auto_20200820_2012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='transaction_id',
            field=models.CharField(max_length=200, null=True, unique=True),
        ),
    ]
