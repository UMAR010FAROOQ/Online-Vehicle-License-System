# Generated by Django 5.0.6 on 2024-05-28 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_customuser_delete_profile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
