# Generated by Django 3.1.1 on 2020-09-22 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_mangement_app', '0002_auto_20200922_0604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leavereportstudent',
            name='leave_status',
            field=models.IntegerField(default=0),
        ),
    ]
