# Generated by Django 3.1.1 on 2020-10-03 13:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student_mangement_app', '0012_auto_20201003_1255'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentinfo',
            name='student_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='student_mangement_app.students'),
            preserve_default=False,
        ),
    ]
