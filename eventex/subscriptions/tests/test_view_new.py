from django.core import mail
from django.test import TestCase
from django.shortcuts import resolve_url as r
from eventex.subscriptions.models import Subscription
from eventex.subscriptions.forms import SubscriptionForm


class SubscriptionsNewGet(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('subscriptions:new'))

    def test_get(self):
        """ Get '/inscricao/' deve retornar status code 200 """
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        """Deve usar subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_html(self):
        """HTML deve conter tags input"""
        tags = (('<form', 1),
                ('<input', 6),
                ('type="text"', 3),
                ('type="email"', 1),
                ('type="submit"', 1))

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)

    def test_csrf(self):
        """Html deve conter CSRF"""
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Contexto deve ter o form de inscricao"""
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)


class SubscriptionsNewPostValid(TestCase):
    def setUp(self):
        data = dict(name='Marcos Ribeiro', cpf='12345678901',
                    email='ribeiro.marcos17@gmail.com', phone='21-98264-7873')
        self.resp = self.client.post(r('subscriptions:new'), data)

    def test_post(self):
        """Um post valido deve redirecionar para '/inscricao/1/'"""
        self.assertRedirects(self.resp, r('subscriptions:detail', 1))

    def test_send_subscribe_mail(self):
        self.assertEqual(1, len(mail.outbox))

    def test_save_subscription(self):
        self.assertTrue(Subscription.objects.exists())


class SubscriptionsNewPostInvalid(TestCase):
    def setUp(self):
        self.resp = self.client.post(r('subscriptions:new'), {})

    def test_post(self):
        """Um post inválido não deve redirecionar"""
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'subscriptions/subscription_form.html')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)

    def test_save_subscription(self):
        self.assertFalse(Subscription.objects.exists())


class TemplateRegressionTest(TestCase):
    def test_template_has_non_field_errors(self):
        invalid_data = dict(name='Marcos Ribeiro', cpf='12345678901')
        response = self.client.post(r('subscriptions:new'), invalid_data)

        self.assertContains(response, '<ul class="errorlist nonfield">')
