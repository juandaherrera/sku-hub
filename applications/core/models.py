from django.db import models
from django_userforeignkey.models.fields import UserForeignKey

# Create your models here.


class LightModelClass(models.Model):
    """
    Project main light model class

    Args:
        models: django model class
    """

    _deleted = models.BooleanField(verbose_name="Borrado", default=False)
    _created_at = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True)
    _updated_at = models.DateTimeField(verbose_name="Fecha de actualización", auto_now=True)
    _deleted_at = models.DateTimeField(verbose_name="Fecha de eliminación", null=True, blank=True)

    class Meta:
        abstract = True


class ModelClass(models.Model):
    """
    Project main model class

    Args:
        models: django model class
    """

    _deleted = models.BooleanField(verbose_name="Borrado", default=False)
    _created_at = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True)
    _updated_at = models.DateTimeField(verbose_name="Fecha de actualización", auto_now=True)
    _deleted_at = models.DateTimeField(verbose_name="Fecha de eliminación", null=True, blank=True)

    _created_by = UserForeignKey(verbose_name="Creado por", auto_user_add=True, related_name="+")
    _updated_by = UserForeignKey(verbose_name="Actualizado por", auto_user=True, related_name="+")

    class Meta:
        abstract = True
