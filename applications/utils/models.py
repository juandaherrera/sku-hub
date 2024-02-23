from django.db import models
from django_userforeignkey.models.fields import UserForeignKey


class LightModelClass(models.Model):
    """
    Project main light model class

    Args:
        models: django model class
    """

    _deleted = models.BooleanField(verbose_name="Borrado", default=False, editable=False)
    _created_at = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True, editable=False)
    _updated_at = models.DateTimeField(verbose_name="Fecha de actualización", auto_now=True, editable=False)

    class Meta:
        abstract = True


class ModelClass(models.Model):
    """
    Project main model class

    Args:
        models: django model class
    """

    _deleted = models.BooleanField(verbose_name="Borrado", default=False, editable=False)
    _created_at = models.DateTimeField(verbose_name="Fecha de creación", auto_now_add=True, editable=False)
    _updated_at = models.DateTimeField(verbose_name="Fecha de actualización", auto_now=True, editable=False)

    _created_by = UserForeignKey(verbose_name="Creado por", auto_user_add=True, related_name="+", editable=False)
    _updated_by = UserForeignKey(verbose_name="Actualizado por", auto_user=True, related_name="+", editable=False)

    class Meta:
        abstract = True
