# Generated by Django 4.0.4 on 2022-04-26 19:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='powerconsumption',
            name='price',
        ),
    ]
