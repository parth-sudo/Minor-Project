# Generated by Django 3.2.2 on 2021-11-30 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_alter_student_answer_sheet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='answer_sheet',
            field=models.FileField(default='sample.pdf', upload_to='student_files'),
        ),
    ]
