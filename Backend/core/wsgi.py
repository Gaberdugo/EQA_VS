import os

from django.core.wsgi import get_wsgi_application
setting_module = 'core.settings'


os.environ.setdefault('DJANGO_SETTINGS_MODULE', setting_module)

application = get_wsgi_application()
