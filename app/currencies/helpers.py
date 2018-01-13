from django.utils import timezone

from .adapters import CsvFileResponseAdapter, PdfFileResponseAdapter
from .models import Currency
from .services import request_updated_rates

"""
CurrenciesHelper

Classe utilitária responsável por executar a lógica necessária para apoiar 
os métodos das views.
"""
class CurrenciesHelper():

    def __init__(self):
        self.supported_currencies = ['USD', 'BRL', 'EUR', 'BTC']
        self.supported_file_formats = ['csv', 'pdf']
        self.default_currency = 'USD'

    """
    Dado o nome de uma moedas como parâmetro, retorna se a moeda é suportada 
    pelo sistema ou não. 
    """
    def is_currency_supported(self, currency_name):
        return self.supported_currencies.__contains__(currency_name)

    """
    Dado o formato de um arquivo como parâmetro, retorna se o formato é 
    suportado pelo sistema ou não. 
    """
    def is_file_format_supported(self, format):
        return self.supported_file_formats.__contains__(format)

    """
    Dado uma lista de parâmetros, então extrai e retorna esses parâmetros do
    objeto request.
    """
    def get_params_from_request(self, request, params_list):
        return [request.GET.get(param) for param in params_list]

    """
    Dado uma lista de parâmetros, então verifica se os parâmetros são válidos.
    """
    def assert_request_params(self, params_list):
        is_valid = True
        for param in params_list:
            if not param:
                is_valid = False
                break
        return is_valid

    """
    Retorna a taxa de conversão entre duas moedas. Caso as taxas ainda não
    existam na base de dados, realiza a consulta em um serviço da web e 
    atualiza o banco de dados local para que seja possível realizar as próximas
    operações sem ter que consultar o serviço da web.
    """
    def get_current_conversion_rate(self, from_currency_name, to_currency_name):
        if not self.rates_up_to_date():
            self.update_currencies_rate()
        from_currency = Currency.objects.get(name=from_currency_name)
        to_currency = Currency.objects.get(name=to_currency_name)
        return to_currency.rate / from_currency.rate

    """
    Verifica se as taxas de conversão entre moedas estão atualizadas baseado
    na data de atualização da moeda de lastro.
    """
    def rates_up_to_date(self):
        if not len(Currency.objects.all()):
            return False
        usd = Currency.objects.get(name=self.default_currency)
        return usd.was_updated_recently()

    """
    Atualiza as taxas de conversão entre as moedas. Caso já exista o registro
    dessas taxas no banco, então atualiza o valor de conversão e a data de
    atualização. Caso contrário, insere as moedas no banco.
    """
    def update_currencies_rate(self):
        rates = request_updated_rates()
        if not len(Currency.objects.all()):
            self.init_rates(rates)
        else:
            self.update_rates(rates)

    """
    Insere as moedas no banco de dados.
    """
    def init_rates(self, rates):
        default_currency = Currency(name=self.default_currency, rate=1, last_update=timezone.now())
        default_currency.save()
        for key, value in rates.items():
            currency_name = key[-3:]
            currency = Currency(name=currency_name, rate=value, last_update=timezone.now())
            currency.save()

    """
    Atualiza o valor de conversão das moedas no banco de dados.
    """
    def update_rates(self, rates):
        default_currency = Currency.objects.get(name=self.default_currency)
        default_currency.last_update = timezone.now()
        default_currency.save()
        for key, value in rates.items():
            currency_name = key[-3:]
            currency = Currency.objects.get(name=currency_name)
            currency.rate = value
            currency.last_update = timezone.now()
            currency.save()

    """
    Dado o valor e a taxa de conversão, então realiza o cálculo para converter
    um valor de uma moeda em outra.
    """
    def convert_value(self, value, rate):
        return float(value) * float(rate)

    """
    Dado o tipo do arquivo, então instancia o adapter correto para exportar o
    conteúdo da conversão de valores.
    """
    def get_file_response_adapter(self, type):
        if type == 'csv':
            return CsvFileResponseAdapter(type)
        elif type == 'pdf':
            return PdfFileResponseAdapter(type)