# Generated by Django 4.0.4 on 2022-06-11 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0005_alter_holiday_head_teacher'),
        ('student', '0006_alter_homeworkstudent_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dailylessons',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacher_daelylessons', to='manager.profile'),
        ),
    ]