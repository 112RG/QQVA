# Generated by Django 4.2 on 2023-07-01 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_command_command_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='command',
            name='command_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]