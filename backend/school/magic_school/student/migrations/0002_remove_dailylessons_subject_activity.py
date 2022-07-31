# Generated by Django 4.0.4 on 2022-07-31 15:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dailylessons',
            name='subject',
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('star', models.IntegerField(blank=True, null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('condition', models.BooleanField(default=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.student')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.subject')),
            ],
        ),
    ]
