# Generated by Django 5.1.7 on 2025-03-12 00:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0003_url'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vacancy',
            options={'ordering': ['-timestamp'], 'verbose_name': 'Вакансия', 'verbose_name_plural': 'Вакансии'},
        ),
    ]
