# Generated by Django 3.0.10 on 2020-10-01 15:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='phone',
        ),
        migrations.RemoveField(
            model_name='account',
            name='picture',
        ),
    ]
