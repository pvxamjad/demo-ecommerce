# Generated by Django 5.1.3 on 2024-11-20 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0007_rename_amount_pay_order_amount_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipped',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='date_orderd',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
