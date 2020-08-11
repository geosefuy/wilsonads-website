# Generated by Django 3.1 on 2020-08-11 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0003_auto_20200811_2107'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='attributes',
            new_name='attribute',
        ),
        migrations.RemoveField(
            model_name='productattribute',
            name='property',
        ),
        migrations.AddField(
            model_name='productattribute',
            name='name',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='productattribute',
            name='value',
            field=models.CharField(max_length=200),
        ),
    ]
