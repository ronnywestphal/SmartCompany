# Generated by Django 4.0.4 on 2022-04-29 13:19

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0004_alter_sectorconsumption_date'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='sectorconsumption',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
    ]