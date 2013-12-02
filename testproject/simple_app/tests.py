"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from .models import Topping, Pizza

class SimpleTest(TestCase):

    def setUp(self):
        self.topping_onion = Topping.objects.get_or_create(name="onion")[0]
        self.topping_egg = Topping.objects.get_or_create(name="egg")[0]

    def test_add_topping(self):
        """tests add a topping"""
        topping = Topping.objects.get_or_create(name="onion")[0]
        self.assertTrue(topping.pk)

    def test_add_pizza_without_toppings(self):
        """test add pizza without topping"""
        pizza = Pizza.objects.get_or_create(name="mussarela")[0]

        self.assertTrue(pizza.pk)

        self.assertEqual(pizza.toppings.all().count(), 0)


    def test_add_pizza_with_toppings(self):
        """test add pizza with topping"""
        pizza = Pizza.objects.get_or_create(name="calabresa")[0]

        self.assertTrue(pizza.pk)

        pizza.toppings.add(self.topping_onion)
        pizza.toppings.add(self.topping_egg)

        self.assertEqual(pizza.toppings.all().count(), 2)