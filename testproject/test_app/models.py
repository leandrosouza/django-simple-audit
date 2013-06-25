# coding: utf-8

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
