# Generated by Django 4.2.1 on 2023-05-20 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ManageEnterprise', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enterprise',
            name='latitud',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='enterprise',
            name='longitud',
            field=models.FloatField(blank=True, null=True),
        ),
    ]