# Generated by Django 2.0.3 on 2018-04-03 20:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_auto_20180403_1417'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='pasta',
            new_name='pastas',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='pasta',
            new_name='pastas',
        ),
    ]
