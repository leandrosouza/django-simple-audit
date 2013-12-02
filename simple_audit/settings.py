"""Settings for django-simple-audit"""
from django.conf import settings

DJANGO_SIMPLE_AUDIT_M2M_FIELDS = getattr(settings, 'DJANGO_SIMPLE_AUDIT_M2M_FIELDS', False)