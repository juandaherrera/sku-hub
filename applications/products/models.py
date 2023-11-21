from django.core.validators import MinValueValidator
from django.db import models

from applications.utils.models import ModelClass


# Create your models here.
class Category(ModelClass):
    """Represents a hierarchical category structure for products.

    Category can have a parent category and a path that is built based on the hierarchy.

    Parameters
    ----------
    ModelClass : django.db.models.Model
        Abstract base class model inherited by Category.

    Attributes
    ----------
    name : models.CharField
        Unique name identifier for the category.
    description : models.TextField
        Optional descriptive text for the category.
    parent : models.ForeignKey
        Optional reference to a parent category, self-referential.
    path : models.CharField
        Stores the hierarchical path of the category, not editable via admin.
    """

    code = models.CharField(max_length=3, unique=True, verbose_name='Código')
    name = models.CharField(max_length=60, unique=True, verbose_name='Nombre')
    description = models.TextField(null=True, blank=True, verbose_name='Descripción')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name='Categoría padre')
    path = models.CharField(max_length=255, editable=False, verbose_name='Path')

    def save(self, *args, **kwargs):
        # Path
        if self.parent:
            self.path = f'{self.parent.path}/{self.name}'
        else:
            self.path = self.name

        # Code
        if self.code:
            self.code = self.code.upper()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.path}'

    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['name']


class Product(ModelClass):
    """Defines the product details and its pricing.

    Includes real price, fake price to simulate discounts, and purchase URLs.

    Parameters
    ----------
    ModelClass : django.db.models.Model
        Abstract base class model inherited by Product.

    Attributes
    ----------
    category : models.ForeignKey
        Category to which the product belongs, can be null.
    name : models.CharField
        The name of the product, can be blank.
    description : models.TextField
        Detailed description of the product, can be blank.
    purchase_urls : models.JSONField
        Stores JSON data with URLs where the product can be purchased.
    stock : models.SmallIntegerField
        Number of units in stock, not editable via admin.
    price_fake : models.DecimalField
        Simulated price before applying discount, can be null or blank.
    price_real : models.DecimalField
        The actual selling price of the product.

    Custom Methods
    -------
    discount_percentage(self) -> float:
        Calculates the discount percentage based on fake and real prices.
    """

    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Categoría')
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name='Nombre')
    description = models.TextField(null=True, blank=True, verbose_name='Descripción')
    purchase_urls = models.JSONField(null=True, blank=True, verbose_name='Links de compra')
    stock = models.SmallIntegerField(default=0, editable=False, verbose_name='Cantidad disponible')
    price_fake = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(100)], blank=True, null=True
    )
    price_real = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(100)])

    def save(self, *args, **kwargs):
        if self.price_fake in [None, '']:
            self.price_fake = self.price_real  # Igualar el precio "falso" al real en caso que no tenga valor.
        if self.price_real > self.price_fake:
            self.price_real, self.price_fake = (
                self.price_fake,
                self.price_real,
            )  # Asegurar que el precio "falso" sea siempre mayor.
        super().save(*args, **kwargs)

    @property
    def discount_percentage(self) -> float:
        if self.price_fake and self.price_real:
            return 1 - (self.price_real / self.price_fake)
        return 0

    def __str__(self) -> str:
        return f'{self.name} ({self.category})'

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        ordering = ['category', 'name', '-price_real']


class Item(ModelClass):
    """Represents a specific item or variant of a product.

    Stores sizes, colors, other attributes, and maintains inventory stock levels.

    Parameters
    ----------
    ModelClass : django.db.models.Model
        Abstract base class model inherited by Item.

    Attributes
    ----------
    product : models.ForeignKey
        Reference to the associated product.
    size : models.CharField
        Size of the item, can be null or blank.
    color : models.CharField
        Color of the item, can be null or blank.
    other_attributes : models.JSONField
        JSON data for any additional attributes of the item.
    stock : models.SmallIntegerField
        Number of units available, not editable via admin.
    price_fake : models.DecimalField
        Simulated price before discount, can be null or blank.
    price_real : models.DecimalField
        The actual selling price of the item.

    Custom Methods
    -------
    discount_percentage(self) -> float:
        Calculates the discount percentage for the item.

    get_other_attributes_as_string(self) -> str:
        Returns a comma-separated string of other attributes.
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Producto')
    size = models.CharField(max_length=20, null=True, blank=True, verbose_name='Talla')
    color = models.CharField(max_length=50, null=True, blank=True, verbose_name='Color')
    other_attributes = models.JSONField(null=True, blank=True, verbose_name='Otros atributos')
    stock = models.SmallIntegerField(default=0, editable=False, verbose_name='Cantidad disponible')
    price_fake = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(100)], blank=True, null=True
    )
    price_real = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(100)], blank=True, null=True
    )

    def save(self, *args, **kwargs):
        if not self.price_fake and not self.price_real:
            self.price_fake, self.price_real = (
                self.product.price_fake,
                self.product.price_real,
            )  # Heredar los precios del producto padre
        elif self.price_fake in [None, '']:
            self.price_fake = self.price_real  # Igualar el precio "falso" al real en caso que no tenga valor.
        elif self.price_real > self.price_fake:
            self.price_real, self.price_fake = (
                self.price_fake,
                self.price_real,
            )  # Asegurar que el precio "falso" sea siempre mayor.
        super().save(*args, **kwargs)

    @property
    def discount_percentage(self) -> float:
        if self.price_fake and self.price_real:
            return 1 - (self.price_real / self.price_fake)
        return 0

    def get_other_attributes_as_string(self) -> str:
        if self.other_attributes:
            return ', '.join(f'{key}: {value}' for key, value in self.other_attributes.items())
        return ''

    def __str__(self) -> str:
        details = []
        if self.size:
            details.append(f'Talla: {self.size}')
        if self.color:
            details.append(f'Color: {self.color}')
        if self.other_attributes:
            details.append(self.get_other_attributes_as_string())

        return f'{self.product} ({", ".join(details)})'

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
        ordering = ['product', 'size', 'color', '-price_real']
