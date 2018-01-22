# coding: utf-8

from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Topping(models.Model):

    name = models.CharField(max_length=50, blank=False, unique=True)

    def __str__(self):
        return self.name
        

@python_2_unicode_compatible
class Pizza(models.Model):

    name = models.CharField(max_length=50, blank=False, unique=True)
    toppings = models.ManyToManyField(Topping)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Message(models.Model):

    title = models.CharField(max_length=50, blank=False)
    text = models.TextField(blank=False)

    def __str__(self):
        return self.text
        

@python_2_unicode_compatible
class Owner(models.Model):

    name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class VirtualMachine(models.Model):

    name = models.CharField(max_length=50, blank=False)
    cpus = models.IntegerField()
    owner = models.ForeignKey(Owner)
    so = models.CharField(max_length=100, blank=False)
    started = models.BooleanField()

    def __str__(self):
        return self.name


