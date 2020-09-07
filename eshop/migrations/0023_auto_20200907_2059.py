# Generated by Django 3.1 on 2020-09-07 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0022_auto_20200904_2033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_ordered',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='instructions',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]
