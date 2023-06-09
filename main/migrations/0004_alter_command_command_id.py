# Generated by Django 4.1.7 on 2023-06-09 05:45

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_command_command'),
    ]

    operations = [
        migrations.AlterField(
            model_name='command',
            name='command_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
