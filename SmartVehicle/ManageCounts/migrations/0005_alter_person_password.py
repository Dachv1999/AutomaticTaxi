# Generated by Django 4.2.1 on 2023-05-22 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ManageCounts', '0004_alter_person_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]