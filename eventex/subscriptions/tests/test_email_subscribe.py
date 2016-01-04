from django.core import mail
from django.test import TestCase


class SubscribePostValid(TestCase):

    def setUp(self):
        data = dict(name='Marcos Ribeiro', cpf='12345678901',
                    email='ribeiro.marcos17@gmail.com', phone='21-98264-7873')
        self.resp = self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        expect = 'Confirmação de inscrição'

        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        expect = 'contato@eventex.com.br'

        self.assertEqual(expect, self.email.from_email)

    def test_subscription_email_to(self):
        expect = ['contato@eventex.com.br', 'ribeiro.marcos17@gmail.com']

        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):
        contents = [
            'Marcos Ribeiro',
            '12345678901',
            'ribeiro.marcos17@gmail.com',
            '21-98264-7873',
        ]
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)
