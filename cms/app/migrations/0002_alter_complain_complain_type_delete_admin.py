# Generated by Django 4.2.5 on 2023-09-20 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complain',
            name='complain_type',
            field=models.CharField(choices=[('Course Content', 'Course Content'), ('Teaching Quality', 'Teaching Quality'), ('Class Scheduling', 'Class Scheduling'), ('Registration Problems', 'Registration Problems'), ('Financial Aid', 'Financial Aid'), ('Administrative Delays', 'Administrative Delays'), ('Housing Conditions', 'Housing Conditions'), ('Facility Issues', 'Facility Issues'), ('Counseling and Health Services', 'Counseling and Health Services'), ('Career Services', 'Career Services'), ('Library and Resources', 'Library and Resources'), ('Student Organizations', 'Student Organizations'), ('Campus Safety', 'Campus Safety'), ('Discrimination', 'Discrimination'), ('Inclusivity', 'Inclusivity'), ('Tuition and Fees', 'Tuition and Fees'), ('Student Employment', 'Student Employment'), ('IT Support', 'IT Support'), ('Grading Disputes', 'Grading Disputes'), ('Transportation Services', 'Transportation Services')], max_length=80),
        ),
        migrations.DeleteModel(
            name='Admin',
        ),
    ]