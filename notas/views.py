from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from django.shortcuts import render, get_object_or_404, redirect
from reportlab.lib.styles import getSampleStyleSheet
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from reportlab.lib.pagesizes import letter
from .models import Nota, ProductoNota
from collections import defaultdict
from reportlab.lib.units import cm
from reportlab.lib import colors
from datetime import datetime
from .forms import NotaForm
from decimal import Decimal
import json
import io


def verNotas(request):
    iva_rate = Decimal("0.16")
    notas = Nota.objects.prefetch_related("productos").all()

    agrupado = defaultdict(
        lambda: {
            "contacto": "",
            "telefono": "",
            "productos": [],
            "cantidad_total": Decimal("0"),
            "anticipo_total": Decimal("0"),
            "subtotal_total": Decimal("0"),
            "iva_total": Decimal("0"),
            "total_total": Decimal("0"),
            "restan_total": Decimal("0"),
            "incluye_iva": False,
        }
    )

    for nota in notas:
        clave = nota.no_trabajo or f"Nota-{nota.id}"
        grupo = agrupado[clave]

        grupo["id"] = nota.id
        grupo["contacto"] = nota.contacto
        grupo["telefono"] = nota.telefono
        grupo["incluye_iva"] = grupo["incluye_iva"] or nota.incluye_iva
        grupo["no_trabajo"] = nota.no_trabajo or f"Nota-{nota.id}"

        subtotal = Decimal("0")
        for producto in nota.productos.all():
            cantidad = Decimal(producto.cantidad or 0)
            precio = Decimal(producto.precio or 0)
            total_producto = Decimal(producto.total or 0)

            grupo["productos"].append(
                {
                    "nombre": producto.nombre,
                    "precio": formatear_numero_ingles(precio),
                    "cantidad": (
                        int(cantidad)
                        if cantidad == int(cantidad)
                        else formatear_numero_ingles(cantidad)
                    ),
                    "total": formatear_numero_ingles(total_producto),
                }
            )

            grupo["cantidad_total"] += cantidad
            subtotal += total_producto

        iva = subtotal * iva_rate if grupo["incluye_iva"] else Decimal("0")
        total = subtotal + iva
        anticipo = Decimal(nota.anticipo or 0)
        restante = total - anticipo

        grupo["subtotal_total"] = formatear_numero_ingles(subtotal)
        grupo["iva_total"] = formatear_numero_ingles(iva)
        grupo["total_total"] = formatear_numero_ingles(total)
        grupo["anticipo_total"] = formatear_numero_ingles(anticipo)
        grupo["restan_total"] = formatear_numero_ingles(restante)

    return render(request, "notas/verNotas.html", {"grupos": dict(agrupado)})


def editar_nota(request, nota_id):
    nota = get_object_or_404(Nota, id=nota_id)
    productos = nota.productos.all()
    form = NotaForm(instance=nota)

    subtotal = sum(p.total for p in productos)
    iva = subtotal * Decimal("0.16") if nota.incluye_iva else Decimal("0")
    total = subtotal + iva
    anticipo = nota.anticipo or Decimal("0")
    restante = total - anticipo

    # Productos formateados
    productos_format = []
    for p in productos:
        productos_format.append(
            {
                "id": p.id,
                "nombre": p.nombre,
                "cantidad": (
                    int(p.cantidad)
                    if p.cantidad == int(p.cantidad)
                    else formatear_numero_ingles(p.cantidad)
                ),
                "precio": formatear_numero_ingles(p.precio),
                "total": formatear_numero_ingles(p.total),
            }
        )

    context = {
        "form": form,
        "nota": nota,
        "productos": productos_format,
        "subtotal": formatear_numero_ingles(subtotal),
        "iva": formatear_numero_ingles(iva),
        "total": formatear_numero_ingles(total),
        "anticipo": formatear_numero_ingles(anticipo),
        "restante": formatear_numero_ingles(restante),
    }
    return render(request, "notas/ModificarNotas.html", context)


def actualizar_nota(request, nota_id):
    if request.method == "POST":
        try:
            nota = Nota.objects.get(id=nota_id)
            data = json.loads(request.body)
            print("📦 Datos recibidos:", data)

            # Actualizar campos de Nota
            nota.tipo = data.get("tipo", nota.tipo)
            nota.entrega = data.get("entrega", nota.entrega)
            nota.pago = data.get("pago", nota.pago)
            nota.anticipo = data.get("anticipo", nota.anticipo)
            nota.incluye_iva = data.get("incluye_iva", nota.incluye_iva)
            nota.fecha = data.get("fecha", nota.fecha)
            nota.contacto = data.get("contacto", nota.contacto)
            nota.telefono = data.get("telefono", nota.telefono)
            nota.factura = data.get("factura", nota.factura)
            nota.no_trabajo = data.get("no_trabajo", nota.no_trabajo)
            nota.save()

            # Eliminar productos actuales asociados a la nota
            ProductoNota.objects.filter(nota=nota).delete()

            # Agregar los nuevos productos
            productos_data = data.get("productos", [])
            for item in productos_data:
                nombre = item.get("producto")  # Aquí el nombre viene directo del JSON
                cantidad = item.get("cantidad", 0)
                precio = item.get("precio", 0)
                total = item.get("total", 0)

                ProductoNota.objects.create(
                    nota=nota,
                    nombre=nombre,
                    cantidad=cantidad,
                    precio=precio,
                    subtotal=cantidad * precio,
                    total=total,
                )

            return JsonResponse(
                {"status": "success", "message": "Nota actualizada correctamente"}
            )

        except Nota.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "Nota no encontrada"}, status=404
            )

        except Exception as e:
            import traceback

            print("💥 Error interno:", traceback.format_exc())
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse(
        {"status": "error", "message": "Método no permitido"}, status=405
    )


def agregar_nota(request):
    print("Request method:", request.method)
    if request.method == "POST":

        data = json.loads(request.body)
        # Parsear fecha
        fecha_str = data.get("fecha", None)
        fecha = None
        if fecha_str:
            try:
                fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            except ValueError:
                fecha = None

        print("Datos recibidos en Django:", data)
        print("Request body:", request.body)

        # Crear la nota principal
        nota = Nota.objects.create(
            tipo=data.get("tipo", ""),
            entrega=data.get("entrega", ""),
            pago=data.get("pago", ""),
            anticipo=data.get("anticipo", 0),
            incluye_iva=data.get("incluye_iva", False),  # cuidado con la clave
            contacto=data.get("contacto", ""),
            telefono=data.get("telefono", ""),
            factura=data.get("factura", ""),
            # no_factura=data.get("no_factura", False),
            no_trabajo=data.get("no_trabajo", ""),
            fecha=data.get("fecha", None),  # <-- Aquí agregas la fecha
        )

        # Guardar productos relacionados
        productos = data.get("productos", [])
        for p in productos:
            ProductoNota.objects.create(
                nota=nota,
                nombre=p.get("producto", ""),
                cantidad=p.get("cantidad", 0),
                precio=p.get("precio", 0),
                total=p.get("total", 0),
            )

        return JsonResponse({"success": True})
    else:
        # Calcular siguiente código no_trabajo para inicializar el formulario
        ultimo_no_trabajo = (
            Nota.objects.filter(no_trabajo__startswith="PG").order_by("-id").first()
        )
        if ultimo_no_trabajo and ultimo_no_trabajo.no_trabajo:
            try:
                numero = int(ultimo_no_trabajo.no_trabajo[2:])
            except ValueError:
                numero = 0
        else:
            numero = 0

        siguiente_codigo = f"PG{numero + 1:02d}"

        form = NotaForm(initial={"no_trabajo": siguiente_codigo})

    return render(request, "notas/AgregarNotas.html", {"form": form})


def formatear_numero_ingles(num):
    """
    Formatea un número Decimal o float a formato inglés:
    16202.23 -> '16,202.23'
    """
    try:
        n = float(num)
    except (ValueError, TypeError):
        return num

    entero, decimal = f"{n:.2f}".split(".")
    entero_con_comas = ""
    while len(entero) > 3:
        entero_con_comas = "," + entero[-3:] + entero_con_comas
        entero = entero[:-3]
    entero_con_comas = entero + entero_con_comas
    return f"{entero_con_comas}.{decimal}"


def generar_pdf_nota(request, nota_id):
    nota = Nota.objects.get(id=nota_id)
    productos = nota.productos.all()

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=letter, rightMargin=2 * cm, leftMargin=2 * cm
    )
    elements = []

    styles = getSampleStyleSheet()
    style_normal = styles["Normal"]
    style_heading = styles["Heading1"]
    style_table_cell = styles["BodyText"]
    style_table_cell.wordWrap = "CJK"  # Para que haga salto de línea

    # Título
    elements.append(Paragraph(f"Nota #{nota.id}", style_heading))
    elements.append(Spacer(1, 12))

    # Info de la nota
    info_fields = [
        f"Trabajo: {nota.no_trabajo or '-'}",
        f"Contacto: {nota.contacto}",
        f"Teléfono: {nota.telefono}",
        f"Fecha: {nota.fecha or '-'}",
        f"Tipo: {nota.tipo}",
        f"Entrega: {nota.entrega}",
        f"Pago: {nota.pago}",
        f"Factura: {nota.factura or ''}",
        f"Incluye IVA: {'Sí' if nota.incluye_iva else 'No'}",
    ]

    for item in info_fields:
        elements.append(Paragraph(item, style_normal))
    elements.append(Spacer(1, 12))

    # Tabla de productos
    data = [
        [
            Paragraph("<b>Producto</b>", style_table_cell),
            Paragraph("<b>Cantidad</b>", style_table_cell),
            Paragraph("<b>Precio</b>", style_table_cell),
            Paragraph("<b>Total</b>", style_table_cell),
        ]
    ]

    subtotal = Decimal("0.00")

    for p in productos:
        cantidad = Decimal(p.cantidad or 0)
        precio = Decimal(p.precio or 0)
        total = Decimal(p.total or 0)

        data.append(
            [
                Paragraph(p.nombre, style_table_cell),
                Paragraph(
                    str(int(cantidad)) if cantidad == cantidad.to_integral() else formatear_numero_ingles(cantidad),
                    style_table_cell
                ),
                Paragraph(f"${formatear_numero_ingles(precio)}", style_table_cell),
                Paragraph(f"${formatear_numero_ingles(total)}", style_table_cell),
            ]
        )

        subtotal += total

    # Definir anchos de columnas: producto = 8cm, el resto más pequeño
    col_widths = [8 * cm, 2.5 * cm, 3 * cm, 3 * cm]

    table = Table(data, colWidths=col_widths)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4CAF50")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )

    elements.append(table)
    elements.append(Spacer(1, 12))

    # Calcular totales con IVA
    iva_rate = Decimal("0.16")
    iva = subtotal * iva_rate if nota.incluye_iva else Decimal("0.00")
    total = subtotal + iva
    anticipo = Decimal(nota.anticipo or 0)
    restante = total - anticipo

    # Totales
    totales = [
        ["Subtotal:", f"${formatear_numero_ingles(subtotal)}"],
        ["IVA (16%):", f"${formatear_numero_ingles(iva)}"],
        ["Total:", f"${formatear_numero_ingles(total)}"],
        ["Anticipo:", f"${formatear_numero_ingles(anticipo)}"],
        ["Restan:", f"${formatear_numero_ingles(restante)}"],
    ]

    for item in totales:
        if item:
            label, value = item
            elements.append(Paragraph(f"<b>{label}</b> {value}", style_normal))

    doc.build(elements)
    buffer.seek(0)
    return HttpResponse(buffer, content_type="application/pdf")


def eliminar_producto(request, producto_id):
    if request.method == "POST":
        try:
            producto = ProductoNota.objects.get(id=producto_id)
            producto.delete()
            return JsonResponse(
                {"status": "success", "message": "Producto eliminado correctamente"}
            )
        except ProductoNota.DoesNotExist:
            return JsonResponse(
                {"status": "error", "message": "Producto no encontrado"}, status=404
            )
    else:
        return JsonResponse(
            {"status": "error", "message": "Método no permitido"}, status=405
        )
