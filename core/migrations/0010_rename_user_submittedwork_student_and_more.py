# Generated by Django 5.1.1 on 2024-09-06 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_submittedwork_date_submitted_submittedwork_updated'),
    ]

    operations = [
        migrations.RenameField(
            model_name='submittedwork',
            old_name='user',
            new_name='student',
        ),
        migrations.AlterField(
            model_name='submittedwork',
            name='file',
            field=models.FileField(upload_to='Projects/%Y/%m/%d'),
        ),
    ]
