from django.apps import AppConfig
from django.contrib.auth import get_user_model


class SimpleAppConfig(AppConfig):
    name = 'testproject.simple_app'
    verbose_name = 'Simple App'

    def ready(self):
        # imports
        from simple_audit.signal import register

        # Get models
        User = get_user_model()
        Message = self.get_model('Message')
        Owner = self.get_model('Owner')
        VirtualMachine = self.get_model('VirtualMachine')
        Pizza = self.get_model('Pizza')
        Topping = self.get_model('Topping')

        # Register with simple_audit
        success = register(Message, Owner, VirtualMachine, User, Pizza, Topping)

