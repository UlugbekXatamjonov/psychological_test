# Generated by Django 3.1 on 2023-01-21 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mytest', '0009_auto_20230121_2224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='info',
            name='test_api',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
