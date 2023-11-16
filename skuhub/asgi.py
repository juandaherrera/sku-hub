"""
ASGI config for skuhub project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.environ.get(
    'SETTINGS_FILE', 'skuhub.settings.local'))

application = get_asgi_application()
