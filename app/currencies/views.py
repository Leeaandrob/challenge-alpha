from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods

from .helpers import CurrenciesHelper
helper = CurrenciesHelper()


"""views.index
Método responsável por retornar a listagem de moedas com as cotações atuais.
"""
@require_http_methods(["GET"])
def index(request):
    return HttpResponse("index page")


"""views.convert
Método que realiza a conversão de um valor em uma determinada moeda para 
outra moeda.

Parâmetros obrigatórios da requisição:
    from: sigla da moeda de origem (Ex. BTC)
    to: sigla da moeda final (Ex. USD)
    value: valor a ser convertido (Ex. 123.45)

Returns:
    <JsonResponse>: Json contendo a moeda de origem, a moeda de destino,
    o valor orignal e o valor convertido.
"""
@require_http_methods(["GET"])
def convert(request):
    from_currency, to_currency, value = helper.get_params_from_request(request, ['from', 'to', 'value'])
    if (not helper.assert_request_params([from_currency, to_currency, value])):
        return JsonResponse({"erro": "Os parâmetros from, to e value são obrigatórios."})

    if not (helper.is_currency_supported(from_currency) and helper.is_currency_supported(to_currency)):
        return JsonResponse({"erro": "As moedas suportadas são USD, BRL, EUR e BTC."})

    rate = helper.get_current_conversion_rate(from_currency, to_currency)
    return JsonResponse({
        "from": from_currency,
        "to": to_currency,
        "originalValue": float(value),
        "convertedValue": helper.convert_value(value, rate)
    })

"""views.convert_and_download
Método que realiza a conversão de um valor em uma determinada moeda para 
outra moeda. As informações são retornadas em forma de arquivo.

Parâmetros obrigatórios da requisição:
    from: sigla da moeda de origem (Ex. BTC)
    to: sigla da moeda final (Ex. USD)
    value: valor a ser convertido (Ex. 123.45)
    type: mime-type do arquivo do donwload

Returns:
    <JsonResponse>: Json contendo a moeda de origem, a moeda de destino,
    o valor orignal e o valor convertido.
"""
@require_http_methods(["GET"])
def convert_and_download(request):
    return JsonResponse({"name": "convert_and_download"})