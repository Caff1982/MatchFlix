# Generated by Django 3.0.10 on 2020-10-17 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flix', '0003_auto_20201010_1450'),
    ]

    operations = [
        migrations.AddField(
            model_name='show',
            name='image',
            field=models.ImageField(default='default.jpg', height_field=750, upload_to='images', width_field=500),
        ),
    ]
