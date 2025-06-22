from django.http import HttpResponse
from .models import Pago
from django.shortcuts import render, redirect, get_object_or_404
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from .forms import PagoForm  # ✅ Importar el formulario aquí
from django.contrib import messages
import io


def generar_pdf_pagos(request):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elementos = []

    styles = getSampleStyleSheet()
    titulo = Paragraph("Lista de Pagos", styles['Heading1'])
    elementos.append(titulo)

    pagos = Pago.objects.all()

    data = [['Título', 'Descripción', 'Fecha de Pago', 'Costo']]

    for pago in pagos:
        data.append([
            pago.titulo,
            pago.descripcion,
            pago.fecha_pago.strftime('%d/%m/%Y'),
            f"${pago.costo:.2f}"
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

def verPagos(request):
    if request.method == 'POST':
        form = PagoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Pago agregado correctamente!')
            return redirect('ver_pago')  # Importante que el nombre coincida en urls.py
    else:
        form = PagoForm()

    pagos = Pago.objects.all()
    return render(request, 'PagosPendientes/VerPagos.html', {'form': form, 'pagos': pagos})

def modificarPago(request, pago_id):
    pago = get_object_or_404(Pago, id=pago_id)

    if request.method == 'POST':
        form = PagoForm(request.POST, instance=pago)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Pago modificado correctamente!')
            return redirect('ver_pago')
    else:
        form = PagoForm(instance=pago)

    return render(request, 'PagosPendientes/ModificarPagos.html', {'form': form})

def eliminarPago(request, pago_id):
    pago = get_object_or_404(Pago, id=pago_id)
    pago.delete()
    return redirect('ver_pago')