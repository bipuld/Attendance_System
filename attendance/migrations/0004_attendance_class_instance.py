# Generated by Django 5.1.1 on 2024-09-16 11:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0003_alter_class_students'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='class_instance',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='attendance.class'),
            preserve_default=False,
        ),
    ]
