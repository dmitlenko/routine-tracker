# Generated by Django 5.1.2 on 2024-10-22 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routines', '0002_alter_routine_options_alter_routineentry_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routine',
            name='measure',
            field=models.CharField(blank=True, default='sec', max_length=50, null=True, verbose_name='Measure'),
        ),
    ]
