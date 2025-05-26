from django.shortcuts import render


def verPagos(request):
    return render(request, 'PagosPendientes/VerPagos.html')

def ModificarPagos(request):
    return render(request, 'PagosPendientes/ModificarPagos.html')