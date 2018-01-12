from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods

"""views.index
Método responsável por retornar a listagem de moedas com as cotações atuais.

Args:
    request: <HttpRequest> objeto que contém as informações da requisição
    
Returns:
    TODO renderizar a página com a listagem
"""
@require_http_methods(["GET"])
def index(request):
    return HttpResponse("index page")


"""views.convert
Método que realiza a conversão de um valor em uma determinada moeda para 
outra moeda.

Args
    request: <HttpRequest> objeto que contém as informações da requisição

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
    from_coin, to_coin, value = getParamsFromRequest(request, ["from", "to", "value"])
    if (not isRequestParamsListValid([from_coin, to_coin, value])):
        return JsonResponse({"erro": "Os parâmetros from, to e value são obrigatórios."})

    rate = getConversionRate()
    return JsonResponse({
        "from": from_coin,
        "to": to_coin,
        "originalValue": float(value),
        "convertedValue": convertValue(value, rate)
    })

"""views.convertAndDownload
Método que realiza a conversão de um valor em uma determinada moeda para 
outra moeda. As informações são retornadas em forma de arquivo.

Args
    request: <HttpRequest> objeto que contém as informações da requisição

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
def convertAndDownload(request):
    return JsonResponse({"name": "convertAndDownload"})

"""getParamsFromRequest
Método que recebe o objeto da requisição e uma lista de parâmetros e retorna 
uma lista com o valor dos parâmetros.

Args:
    request: <HttpRequest>
    paramsList: <Array<String>>
    
Returns:
     <Array<String>> contendo o valor dos parâmetros
"""
def getParamsFromRequest(request, paramsList):
    return [request.GET.get(param) for param in paramsList]

"""TODO
"""
def getConversionRate():
    return 2

"""convertValue
Método que recebe um valor e uma taxa de conversão e retorna o valor convertido. 

Args:
    value: <Float> valor a ser convertido
    rate: <Float> taxa de conversão
    
Returns:
     <Float> valor convertido
"""
def convertValue(value, rate):
    return float(value) * rate

"""isRequestParamsListValid
Método que recebe uma lista de valores e verifica se todos os valores são 
diferentes de null.

Args:
    paramsList: <Array<Object>> lista de valores
    
Returns:
     <Boolean> True caso os valores sejam diferente de null, 
     False caso contrário.
"""
def isRequestParamsListValid(paramsList):
    isValid = True
    for param in paramsList:
        if not param:
            isValid = False
            break

    return isValid