# Generated by Django 4.2 on 2023-07-01 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_command_command_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='command',
            name='command_time',
            field=models.DateField(auto_now_add=True),
        ),
    ]
