from django.shortcuts import render

def verNotas(request):
    return render(request, 'notas/verNotas.html')

def ModificarNotas(request):
    return render(request, 'notas/ModificarNotas.html')

def AgregarNotas(request):
    return render(request, 'notas/AgregarNotas.html')
