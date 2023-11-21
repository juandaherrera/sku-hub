# Payment Choices for PaymentMethod Model
PAYMENT_TYPE_CHOICES = [('EF', 'Efectivo/Transferencia'), ('CR', 'Crédito')]

# Order states
ORDER_STATES = [
    ('finished', 'Finalizada'),
    ('on_the_way', 'En camino'),
    ('draft', 'Borrador'),
    ('cancelled', 'Cancelada'),
]

# Inventory product states
INVENTORY_STATE = [
    ('RFS', 'Ready for Sale'),
    ('RSV', 'Reserved'),
    ('SLD', 'Sold'),
    ('NFS', 'Not for Sale'),
]
