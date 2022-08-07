# Generated by Django 4.0.4 on 2022-08-06 13:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('father_name', models.CharField(blank=True, max_length=30, null=True)),
                ('mother_name', models.CharField(blank=True, max_length=30, null=True)),
                ('certificates', models.CharField(max_length=100)),
                ('job_title', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('birthday', models.DateField()),
                ('gender', models.CharField(choices=[('male', 'male'), ('female', 'female')], default='male', max_length=20)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region=None, unique=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='photo')),
                ('class_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.classroom')),
                ('user', models.ForeignKey(limit_choices_to=models.Q(('account_type', 'employee'), ('account_type', 'teacher'), _connector='OR'), on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QuizName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('class_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='manager.classroom')),
                ('profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='manager.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField()),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='manager.quizname')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('date', models.DateField(auto_now=True)),
                ('timee', models.TimeField(auto_now=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='media')),
                ('user', models.ForeignKey(limit_choices_to={'account_type': 'manager'}, on_delete=django.db.models.deletion.CASCADE, related_name='user_admin_post', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=1200)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('timestamp',),
            },
        ),
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('day', models.DateField()),
                ('description', models.TextField(blank=True, null=True)),
                ('name_of_holiday', models.CharField(max_length=255)),
                ('head_teacher', models.ForeignKey(limit_choices_to={'account_type': 'manager'}, on_delete=django.db.models.deletion.CASCADE, related_name='Holiday_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'modified',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('suggestion', 'suggestion'), ('complaint', 'complaints')], max_length=20)),
                ('text', models.TextField()),
                ('date', models.DateField(auto_now=True, null=True)),
                ('user', models.ForeignKey(limit_choices_to={'account_type': 'manager'}, on_delete=django.db.models.deletion.CASCADE, related_name='manager_feedbacks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
