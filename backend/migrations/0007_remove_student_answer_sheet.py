# Generated by Django 3.2.2 on 2021-12-02 11:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0006_alter_student_answer_sheet'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='answer_sheet',
        ),
    ]
