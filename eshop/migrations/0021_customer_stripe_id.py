# Generated by Django 3.1 on 2020-09-03 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0020_auto_20200903_2241'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='stripe_id',
            field=models.CharField(default='', max_length=200, null=True),
        ),
    ]
