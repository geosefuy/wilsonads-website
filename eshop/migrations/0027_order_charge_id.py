# Generated by Django 3.1 on 2020-09-09 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eshop', '0026_remove_order_transaction_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='charge_id',
            field=models.CharField(default='', max_length=200, null=True),
        ),
    ]
