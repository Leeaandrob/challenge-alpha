import datetime
import requests

from django.test import TestCase
from django.utils import timezone
from django.http import HttpResponse, HttpRequest
from unittest.mock import MagicMock

from .models import Currency
from .helpers import CurrenciesHelper
from .adapters import CsvFileResponseAdapter, PdfFileResponseAdapter


class CurrencyModelTests(TestCase):

    def test_currency_updated_recently(self):
        currency = Currency(name='USD', rate=1, last_update=timezone.now())
        self.assertIs(currency.was_updated_recently(), True)

    def test_currency_not_updated_recently(self):
        currency = Currency(name='USD', rate=1, last_update=timezone.now() - datetime.timedelta(days=1))
        self.assertIs(currency.was_updated_recently(), False)


class CurrenciesHelperTest(TestCase):

    def setup_db(self, helper):
        value = 2
        for currency_name in helper.supported_currencies:
            new_currency = Currency(name=currency_name, rate=value, last_update=timezone.now())
            new_currency.save()
            value += 1

    def test_if_default_properties_are_set(self):
        helper = CurrenciesHelper()
        self.assertEqual(helper.supported_currencies, ['USD', 'BRL', 'EUR', 'BTC'])
        self.assertEqual(helper.supported_file_formats, ['csv', 'pdf'])
        self.assertEqual(helper.default_currency, 'USD')

    def test_get_all_currencies_with_values_from_service(self):
        helper = CurrenciesHelper()

        response = HttpResponse()
        response.json = MagicMock(return_value={
            'quotes': {
                'USDEUR': 2,
                'USDBRL': 3,
                'USDBTC': 4
            }
        })
        requests.get = MagicMock(return_value=response)

        currencies_list = helper.get_all_currencies_with_values()

        response.json.assert_called()
        self.assertIsNotNone(currencies_list)
        self.assertIs(len(Currency.objects.all()), 4)
        for currency in currencies_list:
            self.assertTrue(helper.supported_currencies.__contains__(currency['name']))

        requests.get.assert_called()

    def test_get_all_currencies_with_values_from_db(self):
        helper = CurrenciesHelper()
        self.setup_db(helper)
        requests.get = MagicMock()

        currencies_list = helper.get_all_currencies_with_values()

        self.assertIsNotNone(currencies_list)
        self.assertIs(len(Currency.objects.all()), 4)
        for currency in currencies_list:
            self.assertTrue(helper.supported_currencies.__contains__(currency['name']))

        requests.get.assert_not_called()

    def test_currency_not_supported(self):
        helper = CurrenciesHelper()
        self.assertFalse(helper.is_currency_supported('AAA'))

    def test_currency_supported(self):
        helper = CurrenciesHelper()
        self.assertTrue(helper.is_currency_supported('USD'))

    def test_file_format_not_supported(self):
        helper = CurrenciesHelper()
        self.assertFalse(helper.is_file_format_supported('aaa'))

    def test_file_format_supported(self):
        helper = CurrenciesHelper()
        self.assertTrue(helper.is_file_format_supported('csv'))

    def test_get_params_from_request_without_params_and_assert_not_valid(self):
        helper = CurrenciesHelper()
        request = HttpRequest()
        request.GET.get = MagicMock(return_value=None)

        params_value = helper.get_params_from_request(request, ['param1', 'param2'])
        for value in params_value:
            self.assertIsNone(value)

        self.assertFalse(helper.assert_request_params(params_value))

    def test_get_params_from_request_and_assert_valid(self):
        helper = CurrenciesHelper()
        request = HttpRequest()
        request.GET.get = MagicMock(return_value='value')

        params_value = helper.get_params_from_request(request, ['param1', 'param2'])
        for value in params_value:
            self.assertIsNotNone(value)

        self.assertTrue(helper.assert_request_params(params_value))

    def test_get_current_conversion_rate(self):
        helper = CurrenciesHelper()
        currency_1 = 'USD' # taxa de conversão = 1
        currency_2 = 'EUR' # taxa de conversão igual a 2
        self.setup_db(helper)
        self.assertEqual(helper.get_current_conversion_rate(currency_1, currency_2), 2)
        self.assertEqual(helper.get_current_conversion_rate(currency_2, currency_1), 0.5)

    def test_value_conversion(self):
        helper = CurrenciesHelper()
        currency_1 = 'USD'  # taxa de conversão = 1
        currency_2 = 'EUR'  # taxa de conversão igual a 2
        self.setup_db(helper)
        rate = helper.get_current_conversion_rate(currency_1, currency_2)
        self.assertEqual(helper.convert_value(100, rate), 200)
        self.assertEqual(helper.convert_value(150, rate), 300)

    def test_get_file_response_adapter(self):
        helper = CurrenciesHelper()
        self.assertIsInstance(helper.get_file_response_adapter('csv'), CsvFileResponseAdapter)
        self.assertIsInstance(helper.get_file_response_adapter('pdf'), PdfFileResponseAdapter)
        self.assertIsNone(helper.get_file_response_adapter('aaa'))


class CsvFileResponseAdapterTest(TestCase):

    def test_if_default_properties_are_set(self):
        adapter = CsvFileResponseAdapter()
        self.assertEquals(adapter.default_filename, 'result.csv')
        self.assertIsNotNone(adapter.response)

    def test_get_mime_type(self):
        adapter = CsvFileResponseAdapter()
        self.assertEquals(adapter.get_mime_type(), 'text/csv')

    def test_create_file(self):
        adapter = CsvFileResponseAdapter()
        adapter.create_file()
        self.assertIsNotNone(adapter.writer)

    def test_write_row(self):
        adapter = CsvFileResponseAdapter()
        adapter.create_file()
        adapter.write_row = MagicMock()

        header = ['header1', 'header2', 'header3']
        adapter.write_header(header)
        adapter.write_row.assert_called_with(header)

        content = ['content1', 'content2', 'content3']
        adapter.write_content(content)
        adapter.write_row.assert_called_with(content)

    def test_get_response(self):
        adapter = CsvFileResponseAdapter()
        adapter.create_file()
        self.assertIsInstance(adapter.get_response(), HttpResponse)


class PdfFileResponseAdapterTest(TestCase):

    def test_if_default_properties_are_set(self):
        adapter = PdfFileResponseAdapter()
        self.assertEquals(adapter.default_filename, 'result.pdf')
        self.assertIsNotNone(adapter.response)

    def test_get_mime_type(self):
        adapter = PdfFileResponseAdapter()
        self.assertEquals(adapter.get_mime_type(), 'application/pdf')

    def test_create_file(self):
        adapter = PdfFileResponseAdapter()
        adapter.create_file()
        self.assertIsNotNone(adapter.canvas)

    def test_write_row(self):
        adapter = PdfFileResponseAdapter()
        adapter.create_file()
        adapter.write_row = MagicMock()

        header = ['header1', 'header2', 'header3']
        adapter.write_header(header)
        adapter.write_row.assert_any_call(50, 700, 'header1')
        adapter.write_row.assert_any_call(50, 650, 'header2')
        adapter.write_row.assert_any_call(50, 600, 'header3')

        content = ['content1', 'content2', 'content3']
        adapter.write_content(content)
        adapter.write_row.assert_any_call(200, 700, 'content1')
        adapter.write_row.assert_any_call(200, 650, 'content2')
        adapter.write_row.assert_any_call(200, 600, 'content3')

    def test_get_response(self):
        adapter = PdfFileResponseAdapter()
        adapter.create_file()
        adapter.canvas.showPage = MagicMock()
        adapter.canvas.save = MagicMock()
        self.assertIsInstance(adapter.get_response(), HttpResponse)
        adapter.canvas.showPage.assert_called_once()
        adapter.canvas.save.assert_called_once()
