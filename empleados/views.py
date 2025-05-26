from django.shortcuts import render
from django.http import HttpResponse

def lista_empleados(request):
    return render(request, 'empleados/lista.html')

def nuevo_empleados(request):
    return render(request, 'empleados/AgregarEmpleado.html')

def modificar_empleados(request):
    return render(request, 'empleados/ModificarEmpleado.html')
