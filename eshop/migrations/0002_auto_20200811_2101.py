# Generated by Django 3.1 on 2020-08-11 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productattribute',
            name='name',
        ),
        migrations.AddField(
            model_name='product',
            name='attributes',
            field=models.ManyToManyField(to='eshop.ProductAttribute'),
        ),
        migrations.AddField(
            model_name='productattribute',
            name='property',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='productattribute',
            name='value',
            field=models.CharField(max_length=20),
        ),
    ]
