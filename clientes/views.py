from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponse

def ver_clientes(request):
    return render(request, 'clientes/VerCliente.html')

def nuevo_clientes(request):
    return render(request, 'clientes/AgregarCliente.html')

def modificar_cliente(request):
    return render(request, 'clientes/ModificarCliente.html')
