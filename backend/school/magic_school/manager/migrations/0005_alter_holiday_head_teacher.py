# Generated by Django 4.0.4 on 2022-06-11 11:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('manager', '0004_holiday_head_teacher'),
    ]

    operations = [
        migrations.AlterField(
            model_name='holiday',
            name='head_teacher',
            field=models.ForeignKey(limit_choices_to={'account_type': 'manager'}, on_delete=django.db.models.deletion.CASCADE, related_name='Holiday_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
