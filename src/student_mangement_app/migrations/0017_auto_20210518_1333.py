# Generated by Django 3.1.7 on 2021-05-18 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_mangement_app', '0016_auto_20201011_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='profile_pic',
            field=models.FileField(upload_to='media/student_pic/'),
        ),
    ]
