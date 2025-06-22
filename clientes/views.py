from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from .models import Cliente
from .forms import ClienteForm
import io


def generar_pdf_clientes(request):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elementos = []
    
    styles = getSampleStyleSheet()
    titulo = Paragraph("Lista de Clientes", styles['Heading1'])
    elementos.append(titulo)

    clientes = Cliente.objects.all()

    data = [['Nombre', 'RFC', 'Domicilio', 'Calle', 'Detalles', 'Teléfono']]

    for cliente in clientes:
        data.append([
            cliente.nombre,
            cliente.rfc,
            cliente.domicilio,
            cliente.calle,
            cliente.detalles,
            cliente.telefono
        ])
    
    tabla = Table(data)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elementos.append(tabla)
    doc.build(elementos)

    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')

def ver_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/VerCliente.html', {'clientes': clientes})

def nuevo_clientes(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('misClientes')  # nombre del path en urls.py
    else:
        form = ClienteForm()

    return render(request, 'clientes/AgregarCliente.html', {'form': form})


def modificar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('misClientes')
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'clientes/ModificarCliente.html', {'form': form})

def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    cliente.delete()
    return redirect('misClientes')
