from django.utils import timezone
from django.utils import formats

from .adapters import CsvFileResponseAdapter, PdfFileResponseAdapter
from .models import Currency
from .services import request_updated_rates

class CurrenciesHelper():
    """
    Classe utilitária responsável por executar a lógica necessária para apoiar
    os métodos das views.
    """

    def __init__(self):
        """
        Inicializa os atributos do objeto com valores padrão.
        """
        self.supported_currencies = ['USD', 'BRL', 'EUR', 'BTC']
        self.supported_file_formats = ['csv', 'pdf']
        self.default_currency = 'USD'

    def get_all_currencies_with_values(self):
        if not self.rates_up_to_date(): self.update_currencies_rate()
        currencies = Currency.objects.all()
        currencies_list = []
        for currency in currencies:
            rate = self.get_current_conversion_rate(currency.name, 'BRL')
            c = {
                'name': currency.name,
                'rate': currency.rate,
                'last_update': formats.date_format(currency.last_update, 'd/m/Y'),
                'rate_brl': rate,
                'price_brl': self.convert_value(1, rate)
            }
            currencies_list.append(c)
        return currencies_list


    def is_currency_supported(self, currency_name):
        """
        Dado o nome de uma moedas como parâmetro, retorna se a moeda é suportada
        pelo sistema ou não.
        :param currency_name: nome da moeda
        :return boolean:
        """
        return self.supported_currencies.__contains__(currency_name)

    def is_file_format_supported(self, format):
        """
        Dado o formato de um arquivo como parâmetro, retorna se o formato é
        suportado pelo sistema ou não.
        :param format: formato do arquivo
        :return boolean:
        """
        return self.supported_file_formats.__contains__(format)

    def get_params_from_request(self, request, params_list):
        """
        Dado uma lista de parâmetros, então extrai e retorna esses parâmetros do
        objeto request.
        :param request: objeto da requisição
        :param params_list: lista de parâmetros esperados
        :return list: lista com os valores dos parâmetros
        """
        return [request.GET.get(param) for param in params_list]

    def assert_request_params(self, params_list):
        """
        Dado uma lista de parâmetros, então verifica se os parâmetros são válidos.
        :param params_list: lista com os valores dos parâmetros da requisição
        :return boolean:
        """
        is_valid = True
        for param in params_list:
            if not param:
                is_valid = False
                break
        return is_valid

    def get_current_conversion_rate(self, from_currency_name, to_currency_name):
        """
        Retorna a taxa de conversão entre duas moedas. Caso as taxas ainda não
        existam na base de dados, realiza a consulta em um serviço da web e
        atualiza o banco de dados local para que seja possível realizar as próximas
        operações sem ter que consultar o serviço da web.
        :param from_currency_name: nome da moeda inicial
        :param to_currency_name: nome da moeda destino
        :return float: taxa de conversão entre as moedas
        """
        if not self.rates_up_to_date():
            self.update_currencies_rate()
        from_currency = Currency.objects.get(name=from_currency_name)
        to_currency = Currency.objects.get(name=to_currency_name)
        return to_currency.rate / from_currency.rate

    def rates_up_to_date(self):
        """
        Verifica se as taxas de conversão entre moedas estão atualizadas baseado
        na data de atualização da moeda de lastro.
        :return boolean:
        """
        if not len(Currency.objects.all()):
            return False
        usd = Currency.objects.get(name=self.default_currency)
        return usd.was_updated_recently()

    def update_currencies_rate(self):
        """
        Atualiza as taxas de conversão entre as moedas. Caso já exista o registro
        dessas taxas no banco, então atualiza o valor de conversão e a data de
        atualização. Caso contrário, insere as moedas no banco.
        """
        rates = request_updated_rates()
        if not len(Currency.objects.all()):
            self.init_rates(rates)
        else:
            self.update_rates(rates)

    def init_rates(self, rates):
        """
        Insere as moedas no banco de dados.
        :param rates: taxas de conversão entre a moeda de lastro e as demais
        moedas.
        """
        default_currency = Currency(name=self.default_currency, rate=1, last_update=timezone.now())
        default_currency.save()
        for key, value in rates.items():
            currency_name = key[-3:]
            currency = Currency(name=currency_name, rate=value, last_update=timezone.now())
            currency.save()

    def update_rates(self, rates):
        """
        Atualiza o valor de conversão das moedas no banco de dados.
        :param rates: taxas de conversão entre a moeda de lastro e as demais
        """
        default_currency = Currency.objects.get(name=self.default_currency)
        default_currency.last_update = timezone.now()
        default_currency.save()
        for key, value in rates.items():
            currency_name = key[-3:]
            currency = Currency.objects.get(name=currency_name)
            currency.rate = value
            currency.last_update = timezone.now()
            currency.save()

    def convert_value(self, value, rate):
        """
        Dado o valor e a taxa de conversão, então realiza o cálculo para converter
        um valor de uma moeda em outra.
        :param value: valor a ser convertido
        :param rate: taxa de conversão
        :return float: valor convertido
        """
        return round(float(value) * float(rate), 9)

    def get_file_response_adapter(self, type):
        """
        Dado o tipo do arquivo, então instancia o adapter correto para exportar o
        conteúdo da conversão de valores.
        :param type: tipo do arquivo
        :return: adapter para o tipo de arquivo escolhido
        """
        if type == 'csv':
            return CsvFileResponseAdapter()
        elif type == 'pdf':
            return PdfFileResponseAdapter()