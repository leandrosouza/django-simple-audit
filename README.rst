****************************************
django simple audit
****************************************
This applications was created for audit all changes of models instances and maintain a log of the changes


Installation
===============
You can install django-simple-audit in 2 ways: using pip or by setup.py install

.. code-block:: bash

    $ pip install django-simple-audit


Then modify your settings.py, adding the package `simple_audit` in INSTALLED_APPS and in MIDDLEWARE_CLASSES add
`simple_audit.middleware.threadlocals.RequestThreadLocalMiddleware`:

.. code-block:: bash

	INSTALLED_APPS = (
	    '...',
	    'simple_audit',
	)

	MIDDLEWARE_CLASSES = (
	     '...',
	     'simple_audit.middleware.threadlocals.RequestThreadLocalMiddleware',
	)


Usage
===============

Tracking changes on a model
----------------------------

to audit a model you need import `simple_audit` and then register the model to be audited.

.. code-block:: bash

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


Dependencies
============

* Django == 1.4.x
* django.contrib.contenttypes installed in INSTALLED_APPS
