# Generated by Django 4.1.4 on 2022-12-28 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_account_birthday_account_parent_alter_account_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='birthday',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='Дата рождения'),
        ),
    ]
