# Generated by Django 3.2.2 on 2022-11-07 10:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Blog',
            new_name='Post',
        ),
    ]
