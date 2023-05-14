# Generated by Django 4.2.1 on 2023-05-14 01:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ManageEnterprise', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50)),
                ('money', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('ci', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('date_birth', models.DateField()),
                ('city', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=80, unique=True)),
                ('password', models.CharField(max_length=50)),
                ('home', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('token', models.CharField(max_length=50)),
                ('id_enterprise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ManageEnterprise.enterprise')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('ci', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('date_birth', models.DateField()),
                ('city', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=80, unique=True)),
                ('password', models.CharField(max_length=50)),
                ('home', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('location', models.CharField(max_length=80)),
                ('is_Admin', models.BooleanField(default=False)),
                ('id_wallet', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ManageCounts.wallet')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]