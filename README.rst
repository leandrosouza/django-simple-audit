****************************************
django simple audit
****************************************
This applications was created to audit model's changes and maintain a log of them


Installation
===============
You can install django-simple-audit in 2 ways: using pip or by setup.py install

.. code-block:: bash

    $ pip install django-simple-audit


Then modify your settings.py, adding the package `simple_audit` in INSTALLED_APPS and in MIDDLEWARE_CLASSES add
`simple_audit.middleware.TrackingRequestOnThreadLocalMiddleware`:

.. code-block:: bash

	INSTALLED_APPS = (
	    '...',
	    'simple_audit',
	)

	MIDDLEWARE_CLASSES = (
	     '...',
	     'simple_audit.middleware.TrackingRequestOnThreadLocalMiddleware',
	)

	DJANGO_SIMPLE_AUDIT_ACTIVATED = True

Usage
======

Tracking changes on a model
----------------------------

to audit a model you need import `simple_audit` and then register the model to be audited.

.. code-block:: python

	from django.db import models
	import simple_audit


	class Message(models.Model):

	    title = models.CharField(max_length=50, blank=False)
	    text = models.TextField(blank=False)

	    def __unicode__(self):
	        return self.text


	class Owner(models.Model):

	    name = models.CharField(max_length=50, blank=False)

	    def __unicode__(self):
	        return self.name


	class VirtualMachine(models.Model):

	    name = models.CharField(max_length=50, blank=False)
	    cpus = models.IntegerField()
	    owner = models.ForeignKey(Owner)
	    so = models.CharField(max_length=100, blank=False)
	    started = models.BooleanField()

	    def __unicode__(self):
	        return self.name


	simple_audit.register(Message, Owner, VirtualMachine)

Advanced Usage (without httprequest or our middleware)
--------------------------------------------------------

You can use django-simple-audit without an http request (for example in management command). In this situation
there is no http request on thread context. To ensure gathering all modification on a single AuditRequest, you can
specify it:

.. code-block:: python

	AuditRequest.new_request(path, user, ip)
	try:
	    # my code... in same thread
	finally:
	    AuditRequest.cleanup_request()

Tracking m2m fields changes
----------------------------

Tracking m2m fields changes is still experimental, but you can enable it with the following variable:

    DJANGO_SIMPLE_AUDIT_M2M_FIELDS = True

You need to have at least one cache backend set in your django settings, otherwise the previous settings will be set to False.

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique',
            'TIMEOUT': 300,
        }
    }

Dependencies
============

* Django >= 1.4.x
* django.contrib.contenttypes installed in INSTALLED_APPS


TODO
====
* Improve tests

CHANGELOG
=========
* 0.1.22
	* Fixing admin display Current Content when audited model was deleted ( thanks otherpirate )
* 0.1.21
	* Problems with upload to pypi ( the version was used ) - Sux 

* 0.1.20
        * Add .get_queryset to AuditManager ( thanks sburns )

* 0.1.19
	* Tracking user from Django REST Framework authentication ( thanks jnishiyama )

* 0.1.15
	* use larger TextField for storing values ( thanks dinie )
	* Czech translation ( thanks cuchac )

* 0.1.14
	* improved m2m audit feature ( thanks dinie )
    * Add support for Custom user model ( thanks dinie )
    * Option to turn on/off auditing ( thanks dinie )

* 0.1.12
    * Created some simple tests
    * Enable many to many fiedls tracking (see Usage)
