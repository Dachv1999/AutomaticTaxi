# Generated by Django 4.2.1 on 2023-06-23 04:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ManageEnterprise', '0002_alter_invoice_service_desc'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice_extended',
            name='invoice_id',
        ),
        migrations.DeleteModel(
            name='Invoice',
        ),
        migrations.DeleteModel(
            name='Invoice_extended',
        ),
    ]