# Generated by Django 3.0.10 on 2020-11-10 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='Show',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('show_id', models.CharField(max_length=10)),
                ('is_movie', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=120)),
                ('director', models.CharField(max_length=120)),
                ('release_year', models.IntegerField()),
                ('rating', models.CharField(blank=True, max_length=50, null=True)),
                ('duration', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=250)),
                ('image_url', models.CharField(default='default_image.jpg', max_length=50)),
                ('category', models.ManyToManyField(to='shows.Category')),
                ('country', models.ManyToManyField(to='shows.Country')),
            ],
            options={
                'verbose_name_plural': 'Shows',
                'ordering': ['-release_year'],
            },
        ),
    ]
