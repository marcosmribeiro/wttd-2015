from datetime import datetime

from django.test import TestCase
from eventex.subscriptions.models import Subscription


class SubscriptionModelTest(TestCase):
    def setUp(self):
        self.obj = Subscription(
            name='Marcos Ribeiro',
            cpf='12345678901',
            email='ribeiro.marcos17@gmail.com',
            phone='21982647873'
        )
        self.obj.save()

    def test_create(self):
        self.assertTrue(Subscription.objects.exists())

    def test_created_at(self):
        ''' Subscription deve ter um attributo created_at automatico '''
        self.assertTrue(self.obj.created_at, datetime)

    def test_str(self):
        self.assertEqual('Marcos Ribeiro', str(self.obj))

    def test_paid_default_to_False(self):
        ''' Por default, paid deve ser falso '''
        self.assertFalse(self.obj.paid)
