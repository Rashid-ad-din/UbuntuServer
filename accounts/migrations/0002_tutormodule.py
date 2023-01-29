# Generated by Django 4.1.4 on 2022-12-13 18:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TutorModule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place_of_study', models.CharField(blank=True, max_length=200, null=True, verbose_name='Место учёбы')),
                ('working_place', models.CharField(blank=True, max_length=200, null=True, verbose_name='Место работы')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('changed_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('deleted_at', models.DateTimeField(null=True, verbose_name='Дата удаления')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Удалено')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='tutor', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
    ]