# coding: utf-8
from models import Message, Owner, VirtualMachine
from django.contrib import admin


class MessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'text')


class OwnerAdmin(admin.ModelAdmin):
    list_display = ('name',)


class VirtualMachineAdmin(admin.ModelAdmin):
    list_display = ('name', 'cpus', 'owner')


admin.site.register(Message, MessageAdmin)
admin.site.register(Owner, OwnerAdmin)
admin.site.register(VirtualMachine, VirtualMachineAdmin)
