# Usando o pacote http para renderizar um JSON quando chegar uma requisicao para determinada URL.
from django.http import JsonResponse

# Views.
def clientes(request):
    if request.method == 'GET':
        cliente = {'id': 1, 'nome':'Jao', 'CNPJ': 10000000001, 'email':'teste@gmail.com'}
        return JsonResponse(cliente)
