# Generated by Django 3.1 on 2020-09-15 16:07

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0034_auto_20200915_2344'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='image1',
            field=cloudinary.models.CloudinaryField(default='', max_length=255, verbose_name='image'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='gallery',
            name='image2',
            field=cloudinary.models.CloudinaryField(default='blank', max_length=255, verbose_name='image'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='gallery',
            name='image3',
            field=cloudinary.models.CloudinaryField(default='blank', max_length=255, verbose_name='image'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='homepagebanner',
            name='image',
            field=cloudinary.models.CloudinaryField(default='blank', max_length=255, verbose_name='image'),
            preserve_default=False,
        ),
    ]
