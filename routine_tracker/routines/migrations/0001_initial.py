# Generated by Django 5.1.2 on 2024-10-13 20:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Routine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('icon', models.CharField(blank=True, max_length=50)),
                ('type', models.CharField(choices=[('check', 'Check'), ('time', 'Time'), ('count', 'Count')], default='check', max_length=5)),
                ('has_goal', models.BooleanField(default=False)),
                ('goal', models.PositiveIntegerField(blank=True, null=True)),
                ('measure', models.CharField(blank=True, choices=[('sec', 'Seconds'), ('min', 'Minutes'), ('hrs', 'Hours'), ('rps', 'Reps'), ('sts', 'Sets')], default='sec', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='RoutineEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('value', models.PositiveIntegerField()),
                ('notes', models.TextField(blank=True)),
                ('routine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='routines.routine')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='RoutineGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('icon', models.CharField(blank=True, max_length=50)),
                ('color', models.CharField(default='#007bff', max_length=7)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='routine_groups', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='routine',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='routines', to='routines.routinegroup'),
        ),
    ]
