# Generated by Django 3.2.2 on 2021-11-30 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_student_answer_sheet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='answer_sheet',
            field=models.FileField(upload_to='student_files'),
        ),
    ]