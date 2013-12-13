"""Settings for django-simple-audit"""
import logging
from django.conf import settings

LOG = logging.getLogger(__name__)

DJANGO_SIMPLE_AUDIT_M2M_FIELDS = getattr(settings, 'DJANGO_SIMPLE_AUDIT_M2M_FIELDS', False)

if not hasattr(settings, 'CACHES'):
    LOG.warning("no cache backend set in django! m2m auditing will be disabled")
    DJANGO_SIMPLE_AUDIT_M2M_FIELDS = False