"""
WSGI config for cdv project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
from sys import path

path.append(r'C:\arrimo\cdv')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cdv.settings")
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()