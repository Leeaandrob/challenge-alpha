from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods

from .helpers import CurrenciesHelper
helper = CurrenciesHelper()


@require_http_methods(['GET'])
def index(request):
    """
    Método responsável por retornar a listagem de moedas com as cotações atuais.
    :return HttpResponse:
    """
    context = {'currencies_list': helper.get_all_currencies_with_values()}
    return render(request, 'currencies/index.html', context)

@require_http_methods(['GET'])
def convert(request):
    """
    Método que realiza a conversão de um valor em uma determinada moeda para
    outra moeda.

    Parâmetros obrigatórios da requisição:
        from: sigla da moeda de origem (Ex. BTC)
        to: sigla da moeda final (Ex. USD)
        value: valor a ser convertido (Ex. 123.45)

    :return JsonResponse: Json contendo a moeda de origem, a moeda de destino,
    o valor orignal e o valor convertido.
    """
    from_currency, to_currency, value = helper.get_params_from_request(request, ['from', 'to', 'amount'])
    if (not helper.assert_request_params([from_currency, to_currency, value])):
        return JsonResponse(status=500, data={"erro": "Os parâmetros from, to e amount são obrigatórios."})

    if not (helper.is_currency_supported(from_currency) and helper.is_currency_supported(to_currency)):
        return JsonResponse(status=500, data={"erro": f"As moedas suportadas são {helper.supported_currencies}"})

    rate = helper.get_current_conversion_rate(from_currency, to_currency)
    return JsonResponse({
        "from": from_currency,
        "to": to_currency,
        "originalValue": float(value),
        "convertedValue": helper.convert_value(value, rate),
        "ratesLastUpdatedAt": helper.get_last_time_rates_were_updated()
    })

@require_http_methods(['GET'])
def convert_and_download(request):
    """
    Método que realiza a conversão de um valor em uma determinada moeda para
    outra moeda. As informações são retornadas em forma de arquivo.

    Parâmetros obrigatórios da requisição:
        from: sigla da moeda de origem (Ex. BTC)
        to: sigla da moeda final (Ex. USD)
        value: valor a ser convertido (Ex. 123.45)
        type: mime-type do arquivo do donwload

    :param request:
    :return HttpResponse: reponse contendo o arquivo com as informações
    processadas.
    """
    from_currency, to_currency, value, type = helper.get_params_from_request(request, ['from', 'to', 'amount', 'type'])
    if (not helper.assert_request_params([from_currency, to_currency, value, type])):
        return JsonResponse(status=500, data={"erro": "Os parâmetros from, to, amount e type são obrigatórios."})

    if not (helper.is_currency_supported(from_currency) and helper.is_currency_supported(to_currency)):
        return JsonResponse(status=500, data={"erro": f"As moedas suportadas são {helper.supported_currencies}"})

    if not (helper.is_file_format_supported(type)):
        return JsonResponse(status=500, data={"erro": f"Os formatos de arquivo suportados são {helper.supported_file_formats}."})

    file_adapter = helper.get_file_response_adapter(type)
    file_adapter.create_file()

    header = ['From currency', 'To currency', 'Original Value', 'Converted Value', 'Last time rates were updated']
    file_adapter.write_header(header)

    rate = helper.get_current_conversion_rate(from_currency, to_currency)
    converted_value = helper.convert_value(value, rate)
    last_time_rates_were_updated = helper.get_last_time_rates_were_updated()
    content = [from_currency, to_currency, float(value), converted_value, last_time_rates_were_updated]
    file_adapter.write_content(content)

    return file_adapter.get_response()