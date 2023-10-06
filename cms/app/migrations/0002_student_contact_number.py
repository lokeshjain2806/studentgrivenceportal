# Generated by Django 4.2.5 on 2023-10-06 04:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='contact_number',
            field=models.BigIntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(limit_value=9999999999, message='Contact number is too large.')]),
        ),
    ]