# Generated by Django 3.2.2 on 2021-12-02 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_alter_student_answer_sheet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='answer_sheet',
            field=models.FileField(upload_to='student_files'),
        ),
    ]
