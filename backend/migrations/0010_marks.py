# Generated by Django 3.2.2 on 2022-01-11 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_teacher_teacher_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Marks',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('student_roll_number', models.CharField(max_length=11)),
                ('subject', models.CharField(max_length=30)),
                ('percentage', models.IntegerField()),
            ],
        ),
    ]
