# Generated by Django 4.2.5 on 2023-11-01 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='complain',
            name='createed_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='complain',
            name='complain_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
