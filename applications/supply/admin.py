from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.SupplyPaymentMethod)
admin.site.register(models.Supplier)
admin.site.register(models.SupplyOrder)
admin.site.register(models.SupplyOrderDetail)
admin.site.register(models.Inventory)
