"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from .models import Topping, Pizza
from simple_audit.models import Audit

class SimpleTest(TestCase):

    def setUp(self):
        self.topping_onion = Topping.objects.get_or_create(name="onion")[0]
        self.topping_egg = Topping.objects.get_or_create(name="egg")[0]

        self.content_type_topping = ContentType.objects.get_for_model(Topping)
        self.content_type_pizza = ContentType.objects.get_for_model(Pizza)

    def test_add_topping_and_search_audit(self):
        """tests add a topping"""
        topping = Topping.objects.get_or_create(name="potato")[0]
        
        #topping created
        self.assertTrue(topping.pk)
        #audit recorded?
        self.assertTrue(Audit.objects.get(operation=0, 
                                            content_type=self.content_type_topping,
                                            object_id=topping.pk,
                                            description="Added potato"))

    def test_add_pizza_without_toppings(self):
        """test add pizza without topping"""
        pizza = Pizza.objects.get_or_create(name="mussarela")[0]
        
        #pizza created?
        self.assertTrue(pizza.pk)
        #toppings added?
        self.assertEqual(pizza.toppings.all().count(), 0)
        #audit recorded?
        self.assertTrue(Audit.objects.get(operation=0, 
                                            content_type=self.content_type_pizza,
                                            object_id=pizza.pk,
                                            description="Added mussarela"))


    def test_add_pizza_with_toppings_with_audit_enabled(self):
        """test add pizza with topping"""

        pizza = Pizza.objects.get_or_create(name="peperoni")[0]
        
        #pizza created?
        self.assertTrue(pizza.pk)
        #toppings added?
        pizza.toppings.add(self.topping_onion)

        self.assertEqual(pizza.toppings.all().count(), 1)
        
        #audit recorded?
        self.assertTrue(Audit.objects.get(operation=0, 
                                            content_type=self.content_type_pizza,
                                            object_id=pizza.pk,
                                            description="Added peperoni"))
        
        #m2m audit recorded?
        # field toppings: was changed from None to [{u'id': 2, 'name': u'ovo'}]
        self.assertTrue(Audit.objects.get(operation=1, 
                            content_type=self.content_type_pizza,
                            object_id=pizza.pk,
                            description="field toppings: was changed from None to [{u'id': %s, 'name': u'%s'}]" % (self.topping_onion.id, self.topping_onion.name)))


