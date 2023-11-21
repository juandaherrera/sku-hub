from django.test import TestCase

from .models import Category, Item, Product

# Create your tests here.


class ItemTestCase(TestCase):
    def setUp(self) -> None:
        self.category = Category.objects.create(name='Category test')
        self.product = Product.objects.create(name='Test product', price_real=50000)

    def test_price_fake_correction(self):
        item = Item.objects.create(product=self.product, size='M', color='Rojo', price_fake=30000, price_real=60000)

        self.assertGreaterEqual(
            item.price_fake, item.price_real, "El price_fake debería corregirse para ser igual o mayor que price_real"
        )

    def test_discount_percentage(self):
        item = Item.objects.create(product=self.product, size='M', color='Rojo', price_fake=120000, price_real=90000)

        self.assertEqual(
            item.discount_percentage,
            0.25,
            "La propiedad discount_percentage debería corregirse para que represente el verdadero porcentaje de\
            descuento (1 - (price_real/price_Fake))",
        )
