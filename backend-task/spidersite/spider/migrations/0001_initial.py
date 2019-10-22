# Generated by Django 2.2.6 on 2019-10-18 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=130)),
                ('page_title', models.CharField(max_length=120)),
                ('title', models.CharField(max_length=120)),
                ('speaker', models.CharField(max_length=50)),
                ('announce_date', models.DateField()),
                ('time', models.CharField(max_length=50)),
                ('room', models.CharField(max_length=50)),
            ],
        ),
    ]