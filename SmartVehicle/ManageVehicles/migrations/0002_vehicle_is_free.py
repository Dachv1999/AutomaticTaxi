# Generated by Django 4.2.1 on 2023-05-20 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ManageVehicles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='is_free',
            field=models.BooleanField(default=True),
        ),
    ]