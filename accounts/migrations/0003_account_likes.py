# Generated by Django 3.0.10 on 2020-10-04 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flix', '0001_initial'),
        ('accounts', '0002_auto_20201001_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='likes',
            field=models.ManyToManyField(blank=True, to='flix.Show'),
        ),
    ]