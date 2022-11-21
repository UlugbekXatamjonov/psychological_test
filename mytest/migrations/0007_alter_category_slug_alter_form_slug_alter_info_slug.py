# Generated by Django 4.1.2 on 2022-11-21 12:48

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mytest', '0006_test_test_answer_test_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True),
        ),
        migrations.AlterField(
            model_name='form',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='name', unique=True),
        ),
        migrations.AlterField(
            model_name='info',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='full_name', unique=True),
        ),
    ]
