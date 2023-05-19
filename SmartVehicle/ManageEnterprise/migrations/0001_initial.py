# Generated by Django 4.2.1 on 2023-05-18 02:36

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Enterprise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enterprise_name', models.CharField(max_length=25, unique=True)),
                ('email', models.EmailField(max_length=80, unique=True)),
                ('cuenta', models.CharField(max_length=255, null=True, unique=True)),
                ('private_key', models.CharField(max_length=255, null=True, unique=True)),
                ('budget', models.DecimalField(decimal_places=2, max_digits=8)),
                ('longitud', models.CharField(blank=True, max_length=80, null=True)),
                ('latitud', models.CharField(blank=True, max_length=80, null=True)),
                ('taxes', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('nit', models.PositiveIntegerField(primary_key=True, serialize=False, validators=[django.core.validators.MinValueValidator(10000), django.core.validators.MaxValueValidator(99999)])),
                ('service_desc', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id_empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ManageEnterprise.enterprise')),
            ],
        ),
    ]
