# Generated by Django 5.1.3 on 2024-11-19 08:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_rename_address1_shaippingaddress_shipping_address1_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shaippingaddress',
            old_name='shipping_full_name',
            new_name='shipping_fisrt_name',
        ),
    ]
