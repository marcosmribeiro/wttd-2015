from django.test import TestCase
from eventex.subscriptions.admin import SubscriptionModelAdmin, Subscription, admin
from unittest.mock import Mock

class SubscriptionModelAdminTest(TestCase):
    def setUp(self):
        Subscription.objects.create(name='Marcos Ribeiro', cpf='12345678901',
                                    email='ribeiro.marcos17@gmail.com', phone='21-982647873')
        self.model_admin = SubscriptionModelAdmin(Subscription, admin.site)

    def test_has_action(self):
        ''' A Action mark_as_paid deve estar instalado '''
        self.assertIn('mark_as_paid', self.model_admin.actions)

    def test_mark_all(self):
        ''' Deve marcar todas as inscrições como paga '''
        self.call_action()

        self.assertEqual(1, Subscription.objects.filter(paid=True).count())

    def test_message(self):
        ''' Deve enviar uma mensagem para o usuário '''
        mock = self.call_action()

        mock.assert_called_once_with(None, '1 inscrição foi marcada como paga.')

    def call_action(self):
        queryset = Subscription.objects.all()

        mock = Mock()
        old_message_user = SubscriptionModelAdmin.message_user
        SubscriptionModelAdmin.message_user = mock

        self.model_admin.mark_as_paid(None, queryset)

        SubscriptionModelAdmin.message_user = old_message_user

        return mock
