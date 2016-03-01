"""Settings for django-simple-audit"""
import logging
from django.conf import settings

LOG = logging.getLogger(__name__)

DJANGO_SIMPLE_AUDIT_ACTIVATED = getattr(settings, 'DJANGO_SIMPLE_AUDIT_ACTIVATED', False)
DJANGO_SIMPLE_AUDIT_M2M_FIELDS = getattr(settings, 'DJANGO_SIMPLE_AUDIT_M2M_FIELDS', False)

"""
  DJANGO_SIMPLE_AUDIT_REST_FRAMEWORK_AUTHENTICATOR setting should be set to 
  Django REST Framework authentication class if framework is being used

  e.g. in myproj.settings 
  DJANGO_SIMPLE_AUDIT_REST_FRAMEWORK_AUTHENTICATOR = 'rest_framework.authentication.TokenAuthentication'
"""
DJANGO_SIMPLE_AUDIT_REST_FRAMEWORK_AUTHENTICATOR = getattr(settings, 'DJANGO_SIMPLE_AUDIT_AUTHENTICATOR', None)

if not hasattr(settings, 'CACHES'):
    LOG.warning("no cache backend set in django! m2m auditing will be disabled")
    DJANGO_SIMPLE_AUDIT_M2M_FIELDS = False
