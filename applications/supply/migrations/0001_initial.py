# Generated by Django 4.2.7 on 2023-11-21 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_deleted', models.BooleanField(default=False, editable=False, verbose_name='Borrado')),
                ('_created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('_updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
                ('batch_code', models.CharField(editable=False, max_length=7, unique=True, verbose_name='Código de Lote')),
                ('entries', models.SmallIntegerField(editable=False, verbose_name='Entradas')),
                ('exits', models.SmallIntegerField(default=0, editable=False, verbose_name='Salidas')),
                ('stock', models.SmallIntegerField(editable=False, verbose_name='Inventario Actual')),
                ('unit_cost', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Costo')),
                ('last_entry_at', models.DateTimeField(verbose_name='Última entrada')),
                ('last_exit_at', models.DateTimeField(verbose_name='Última salida')),
                ('state', models.CharField(choices=[('RFS', 'Ready for Sale'), ('RSV', 'Reserved'), ('SLD', 'Sold'), ('NFS', 'Not for Sale')], default='RFS', max_length=3, verbose_name='Estado')),
            ],
            options={
                'verbose_name': 'Inventario',
                'verbose_name_plural': 'Inventarios',
                'ordering': ['item', 'last_entry_at', 'last_exit_at', '-unit_cost'],
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_deleted', models.BooleanField(default=False, editable=False, verbose_name='Borrado')),
                ('_created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('_updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
                ('name', models.CharField(max_length=100, verbose_name='Nombre')),
                ('main_url', models.URLField(blank=True, null=True, verbose_name='URL principal')),
            ],
            options={
                'verbose_name': 'Proveedor',
                'verbose_name_plural': 'Proveedores',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='SupplyOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_deleted', models.BooleanField(default=False, editable=False, verbose_name='Borrado')),
                ('_created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('_updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
                ('order_date', models.DateField(verbose_name='Fecha de la orden')),
                ('sub_total', models.DecimalField(decimal_places=2, editable=False, max_digits=12, verbose_name='Sub total')),
                ('shipping_fee', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Costo de envío')),
                ('taxes', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Impuestos')),
                ('total', models.DecimalField(decimal_places=2, editable=False, max_digits=12, verbose_name='Total')),
                ('related_urls', models.JSONField(blank=True, null=True, verbose_name='Links de compra')),
                ('trm', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True, verbose_name='TRM')),
                ('state', models.CharField(choices=[('finished', 'Finalizada'), ('on_the_way', 'En camino'), ('draft', 'Borrador'), ('cancelled', 'Cancelada')], max_length=16, verbose_name='Estado')),
            ],
            options={
                'verbose_name': 'Orden de compra',
                'verbose_name_plural': 'Órdenes de compra',
                'ordering': ['-order_date', '-total'],
            },
        ),
        migrations.CreateModel(
            name='SupplyOrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_deleted', models.BooleanField(default=False, editable=False, verbose_name='Borrado')),
                ('_created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('_updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
                ('quantity', models.SmallIntegerField(verbose_name='Cantidad')),
                ('unit_cost', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Costo unitario')),
                ('sub_total', models.DecimalField(decimal_places=2, editable=False, max_digits=12, verbose_name='Sub total')),
                ('shipping_fee', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Costo de envío')),
                ('taxes', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Impuestos')),
                ('total', models.DecimalField(decimal_places=2, max_digits=12, verbose_name='Costo total')),
                ('purchase_url', models.URLField(blank=True, null=True, verbose_name='Link de compra')),
            ],
            options={
                'verbose_name': 'Detalle orden de compra',
                'verbose_name_plural': 'Detalles orden de compra',
                'ordering': ['order', '-total'],
            },
        ),
        migrations.CreateModel(
            name='SupplyPaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_deleted', models.BooleanField(default=False, editable=False, verbose_name='Borrado')),
                ('_created_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('_updated_at', models.DateTimeField(auto_now=True, verbose_name='Fecha de actualización')),
                ('name', models.CharField(max_length=60, verbose_name='Nombre')),
                ('type', models.CharField(choices=[('EF', 'Efectivo/Transferencia'), ('CR', 'Crédito')], max_length=2, verbose_name='Tipo')),
            ],
            options={
                'verbose_name': 'Método de pago',
                'verbose_name_plural': 'Métodos de pago',
                'ordering': ['name'],
            },
        ),
    ]
