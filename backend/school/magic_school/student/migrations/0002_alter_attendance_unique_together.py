# Generated by Django 4.0.4 on 2022-08-06 21:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together={('student', 'day')},
        ),
    ]
