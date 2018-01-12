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
    return JsonResponse({"name": "convert"})

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