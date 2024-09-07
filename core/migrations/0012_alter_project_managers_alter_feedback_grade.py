# Generated by Django 5.1.1 on 2024-09-07 02:46

import django.db.models.manager
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_rename_students_supervisor_student'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='project',
            managers=[
                ('active_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='feedback',
            name='grade',
            field=models.CharField(choices=[('A+', 'A+'), ('A', 'A'), ('b+', 'B+'), ('B', 'B'), ('c', 'C'), ('D', 'D'), ('F', 'F')], max_length=5),
        ),
    ]
