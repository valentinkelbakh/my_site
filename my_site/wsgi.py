"""
WSGI config for my_site project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""
import sys
path = '/home/valentinkelbakh/my_site'
if path not in sys.path:
    sys.path.insert(0, path)

import os
from django.core.wsgi import get_wsgi_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "my_site.settings")
application = get_wsgi_application()
