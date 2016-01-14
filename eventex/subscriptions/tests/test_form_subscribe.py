from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscriptionFormTest(TestCase):
    def test_form_has_fields(self):
        """Form deve ter 4 campos"""
        form = SubscriptionForm()
        expected = ['name', 'cpf', 'email', 'phone']
        self.assertSequenceEqual(expected, list(form.fields))

    def test_cpf_is_digit(self):
        """CPF deve aceitar apenas digitos."""
        form = self.make_validated_form(cpf='ABCD5678901')
        field = 'cpf'
        code = 'digits'
        self.assertFormErrorCode(form, field, code)

    def test_cpf_has_11_digits(self):
        """CPF deve ter 11 digitos"""
        form = self.make_validated_form(cpf='1234')
        field = 'cpf'
        code = 'length'
        self.assertFormErrorCode(form, field, code)

    def assertFormErrorCode(self, form, field, code):
        errors = form.errors.as_data()
        errors_list = errors[field]
        exception = errors_list[0]
        self.assertEqual(code, exception.code)

    def assertFormErrorMessage(self, form, field, msg):
        errors = form.errors
        errors_list = errors[field]
        self.assertListEqual([msg], errors_list)

    def make_validated_form(self, **kwargs):
        valid = dict(name='Marcos Ribeiro', cpf='12345678901',
                     email='ribeiro.marcos17@gmail.com', phone='21-982647873')
        data = (dict(valid, **kwargs))
        form = SubscriptionForm(data)
        form.is_valid()

        return form
