# Generated by Django 5.1.1 on 2024-10-08 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facturacion', '0002_alter_contrato_estado_alter_factura_estado'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='id',
        ),
        migrations.AlterField(
            model_name='usuario',
            name='cedula',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
