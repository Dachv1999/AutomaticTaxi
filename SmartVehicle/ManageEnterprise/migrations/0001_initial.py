# Generated by Django 4.2.1 on 2023-06-08 04:37

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
                ('longitud', models.FloatField(blank=True, null=True)),
                ('latitud', models.FloatField(blank=True, null=True)),
                ('taxes', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nit', models.CharField(max_length=255, null=True, unique=True)),
                ('service_desc', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('is_pay', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id_empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ManageEnterprise.enterprise')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice_extended',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ManageEnterprise.invoice')),
            ],
        ),
    ]
