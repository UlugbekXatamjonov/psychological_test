# Generated by Django 3.1 on 2023-01-21 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mytest', '0003_auto_20230121_2126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='test_api',
            field=models.JSONField(default=1),
            preserve_default=False,
        ),
    ]