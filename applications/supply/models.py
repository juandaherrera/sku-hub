import secrets
import string

from django.db import models

from applications.products.models import Item
from applications.utils.models import ModelClass

from .choices import INVENTORY_STATE, ORDER_STATES, PAYMENT_TYPE_CHOICES

# Create your models here.


class SupplyPaymentMethod(ModelClass):
    name = models.CharField(max_length=60, verbose_name='Nombre')
    type = models.CharField(max_length=2, choices=PAYMENT_TYPE_CHOICES, verbose_name='Tipo')

    class Meta:
        verbose_name = 'Método de pago'
        verbose_name_plural = 'Métodos de pago'
        ordering = ['name']


class Supplier(ModelClass):
    name = models.CharField(max_length=100, verbose_name='Nombre')
    main_url = models.URLField(verbose_name='URL principal', null=True, blank=True)

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['name']


class SupplyOrder(ModelClass):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, verbose_name='Proveedor')
    order_date = models.DateField(verbose_name='Fecha de la orden')
    payment_method = models.ForeignKey(SupplyPaymentMethod, on_delete=models.CASCADE, verbose_name='Método de pago')
    sub_total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Sub total', editable=False)
    shipping_fee = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Costo de envío')
    taxes = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Impuestos')
    total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Total', editable=False)
    related_urls = models.JSONField(null=True, blank=True, verbose_name='Links de compra')
    trm = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True, verbose_name='TRM')
    state = models.CharField(max_length=16, choices=ORDER_STATES, verbose_name='Estado')

    @property
    def taxes_percentage(self) -> float:
        if self.taxes and self.taxes > 0:
            return self.taxes / self.sub_total
        return 0

    class Meta:
        verbose_name = 'Orden de compra'
        verbose_name_plural = 'Órdenes de compra'
        ordering = ['-order_date', '-total']


class SupplyOrderDetail(ModelClass):
    order = models.ForeignKey(SupplyOrder, on_delete=models.CASCADE, verbose_name='Orden')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Item')
    quantity = models.SmallIntegerField(verbose_name='Cantidad')
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Costo unitario')
    sub_total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Sub total', editable=False)
    shipping_fee = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Costo de envío')
    taxes = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Impuestos')
    total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Costo total')
    purchase_url = models.URLField(verbose_name='Link de compra', null=True, blank=True)

    class Meta:
        verbose_name = 'Detalle orden de compra'
        verbose_name_plural = 'Detalles orden de compra'
        ordering = ['order', '-total']


class Inventory(ModelClass):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Item')
    supply_order_detail = models.ForeignKey(
        SupplyOrderDetail, on_delete=models.CASCADE, verbose_name='Detalle de Orden de Compra'
    )
    batch_code = models.CharField(max_length=7, unique=True, editable=False, verbose_name='Código de Lote')
    entries = models.SmallIntegerField(editable=False, verbose_name='Entradas')
    exits = models.SmallIntegerField(editable=False, default=0, verbose_name='Salidas')
    stock = models.SmallIntegerField(editable=False, verbose_name='Inventario Actual')
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Costo')
    last_entry_at = models.DateTimeField(verbose_name='Última entrada')
    last_exit_at = models.DateTimeField(verbose_name='Última salida')
    state = models.CharField(max_length=3, choices=INVENTORY_STATE, default='RFS', verbose_name='Estado')

    @property
    def total_cost(self) -> float:
        return self.stock * self.unit_cost

    def _generate_batch_code(self):
        first_part = self.item.product.category.code
        second_part = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(3))
        return f'{first_part}-{second_part}'.upper()

    def save(self, *args, **kwargs):
        if not self.batch_code:
            # Genera un batch_code único
            batch_code = self._generate_batch_code()
            while Inventory.objects.filter(batch_code=batch_code).exists():
                batch_code = self._generate_batch_code()
            self.batch_code = batch_code
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Inventario'
        verbose_name_plural = 'Inventarios'
        ordering = ['item', 'last_entry_at', 'last_exit_at', '-unit_cost']
