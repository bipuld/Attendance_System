# Generated by Django 5.1.1 on 2024-09-19 03:18

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0004_attendance_class_instance'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='class',
            name='created_by',
            field=models.ForeignKey(db_column='created_by', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='classes_created', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='class',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='student',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='student',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='students', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='attendance',
            unique_together={('student', 'class_instance', 'date')},
        ),
    ]
