from django.http import HttpResponse
from django.shortcuts import render, redirect,  get_object_or_404
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from .models import Empleado
from .forms import EmpleadoForm
import io


def generar_pdf_empleados(request):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elementos = []
    
    styles = getSampleStyleSheet()
    titulo = Paragraph("Lista de Empleados", styles['Heading1'])
    elementos.append(titulo)

    # Obtener empleados
    empleados = Empleado.objects.all()
    
    # Encabezados de la tabla
    data = [['Nombre', 'Apellido Paterno', 'Apellido Materno', 'Edad', 'Teléfono', 'Cargo', 'N° Cuenta', 'Banco']]
    
    # Filas de la tabla
    for emp in empleados:
        data.append([
            emp.nombre,
            emp.apellido_paterno,
            emp.apellido_materno,
            str(emp.edad),
            emp.telefono,
            emp.cargo,
            emp.numero_cuenta,
            emp.nombre_banco
        ])
    
    # Crear tabla
    tabla = Table(data)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elementos.append(tabla)
    doc.build(elementos)

    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')

def lista_empleados(request):
    empleados = Empleado.objects.all()
    return render(request, 'empleados/lista.html', {'empleados': empleados})

def nuevo_empleados(request):
    if request.method == 'POST':
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_empleados')
    else:
        form = EmpleadoForm()
    return render(request, 'empleados/AgregarEmpleado.html', {'form': form, 'accion': 'Agregar'})

def modificar_empleados(request, id):
    empleado = get_object_or_404(Empleado, pk=id)
    if request.method == 'POST':
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            return redirect('lista_empleados')
    else:
        form = EmpleadoForm(instance=empleado)
    return render(request, 'empleados/ModificarEmpleado.html', {'form': form, 'accion': 'Modificar'})


def eliminar_empleado(request, id):
    empleado = get_object_or_404(Empleado, pk=id)
    empleado.delete()
    return redirect('lista_empleados')
