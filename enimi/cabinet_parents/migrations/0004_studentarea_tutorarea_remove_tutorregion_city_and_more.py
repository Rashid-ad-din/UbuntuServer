# Generated by Django 4.1.4 on 2023-01-03 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cabinet_parents', '0003_alter_survey_max_cost_alter_survey_min_cost'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('student_city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_areas', to='cabinet_parents.city', verbose_name='Город')),
                ('student_district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_areas', to='cabinet_parents.district', verbose_name='Район')),
                ('student_region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_areas', to='cabinet_parents.region', verbose_name='Область')),
            ],
        ),
        migrations.CreateModel(
            name='TutorArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('tutor_city', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tutor_areas', to='cabinet_parents.city', verbose_name='Город')),
                ('tutor_district', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tutor_areas', to='cabinet_parents.district', verbose_name='Район')),
                ('tutor_region', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tutor_areas', to='cabinet_parents.region', verbose_name='Область')),
            ],
        ),
        migrations.RemoveField(
            model_name='tutorregion',
            name='city',
        ),
        migrations.RemoveField(
            model_name='tutorregion',
            name='district',
        ),
        migrations.RemoveField(
            model_name='tutorregion',
            name='region',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='student_region',
        ),
        migrations.RemoveField(
            model_name='survey',
            name='tutor_region',
        ),
        migrations.AlterField(
            model_name='survey',
            name='education_time',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='surveys', to='cabinet_parents.educationtime', verbose_name='Время для обучения'),
        ),
        migrations.DeleteModel(
            name='StudentRegion',
        ),
        migrations.DeleteModel(
            name='TutorRegion',
        ),
        migrations.AddField(
            model_name='survey',
            name='student_area',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='surveys', to='cabinet_parents.studentarea', verbose_name='Район занятий у ученика'),
        ),
        migrations.AddField(
            model_name='survey',
            name='tutor_area',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='surveys', to='cabinet_parents.tutorarea', verbose_name='Район занятий у репетитора'),
        ),
    ]
