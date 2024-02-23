from django.db import models
from django.contrib.auth.models import AbstractUser

LATIN_AMERICA = (
    ('AR', 'Argentina'),
    ('BO', 'Bolivia'),
    # ('BR', 'Brasil'),
    ('CL', 'Chile'),
    ('CO', 'Colombia'),
    ('CR', 'Costa Rica'),
    ('CU', 'Cuba'),
    ('DO', 'República Dominicana'),
    ('EC', 'Ecuador'),
    ('SV', 'El Salvador'),
    ('GT', 'Guatemala'),
    ('HT', 'Haití'),
    ('HN', 'Honduras'),
    ('MX', 'México'),
    ('NI', 'Nicaragua'),
    ('PA', 'Panamá'),
    ('PY', 'Paraguay'),
    ('PE', 'Perú'),
    ('PR', 'Puerto Rico'),
    ('UY', 'Uruguay'),
    ('VE', 'Venezuela'),
)

# Create your models here.


class CustomUser(AbstractUser):
    """
    Custom class to modified Django's default user

    Args:
        AbstractUser: default Django's abstract user
    """
    country = models.CharField(
        verbose_name="País de origen", default='CO', choices=LATIN_AMERICA, max_length=2)
