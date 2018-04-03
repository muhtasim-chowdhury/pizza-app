# Generated by Django 2.0.3 on 2018-04-02 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_auto_20180402_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='sub',
            name='isMenu',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='sub',
            name='price',
            field=models.DecimalField(decimal_places=2, default=6.5, max_digits=4),
        ),
    ]
