# Generated by Django 5.0.6 on 2024-06-12 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_learningmaterial_file_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FeeStructure',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=20)),
                ('testFee', models.CharField(max_length=20)),
                ('afterPassingTest', models.CharField(max_length=20)),
                ('courierFee', models.CharField(max_length=20)),
                ('totalFee', models.CharField(max_length=20)),
            ],
        ),
    ]
