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

    def test_name_must_be_captalized(self):
        """O nome deve conter iniciais maiúsculas"""
        # MARCOS ribeiro -> Marcos Ribeiro
        form = self.make_validated_form(name='MARCOS ribeiro')
        self.assertEqual('Marcos Ribeiro', form.cleaned_data['name'])

    def test_email_is_optional(self):
        form = self.make_validated_form(email='')
        self.assertFalse(form.errors)

    def test_phone_is_optional(self):
        form = self.make_validated_form(phone='')
        self.assertFalse(form.errors)

    def test_must_inform_email_or_phone(self):
        """Email e Phone são opcionais, mas deve haver ao menos 1 dos 2"""
        form = self.make_validated_form(email='', phone='')
        self.assertListEqual(['__all__'], list(form.errors))

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
