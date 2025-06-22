from django.db import models

TIPO_CHOICES = [
    ('ANUNCIO 2D', 'ANUNCIO 2D'),
    ('ANUNCIO LUMINOSO', 'ANUNCIO LUMINOSO'),
    ('ARTICULOS PUBLICITARIOS', 'ARTICULOS PUBLICITARIOS'),
    ('BANDERA PUBLICITARIA', 'BANDERA PUBLICITARIA'),
    ('DISEÑO', 'DISEÑO'),
    ('ELECTROSTATICO', 'ELECTROSTATICO'),
    ('ESTRUCTURA CON LONA', 'ESTRUCTURA CON LONA'),
    ('ETIQUETAS', 'ETIQUETAS'),
    ('LETRAS 3D', 'LETRAS 3D'),
    ('LONA', 'LONA'),
    ('MICROPERFORADO', 'MICROPERFORADO'),
    ('NOTA', 'NOTA'),
    ('PROMOCIONALES', 'PROMOCIONALES'),
    ('SELLO', 'SELLO'),
    ('SEÑALETICA', 'SEÑALETICA'),
    ('SERIGRAFIA', 'SERIGRAFIA'),
    ('TABLOIDES', 'TABLOIDES'),
    ('TARJETA', 'TARJETA'),
    ('TAZAS', 'TAZAS'),
    ('TEXTIL', 'TEXTIL'),
    ('TOLDO ENROLLABLE', 'TOLDO ENROLLABLE'),
    ('TOLDO FIJO', 'TOLDO FIJO'),
    ('VINIL CON SUAJE', 'VINIL CON SUAJE'),
    ('VINIL CORTE', 'VINIL CORTE'),
    ('VINIL IMPRESO', 'VINIL IMPRESO'),
    ('PLAYERAS', 'PLAYERAS'),
    ('VOLANTE', 'VOLANTE'),
]

ENTREGA = [
    ('Domicilio', 'Domicilio'),
    ('Galindas', 'Galindas'),
    ('Instalacion', 'Instalacion'),
]

PAGO = [
    ('Trasferencia', 'Trasferencia'),
    ('Tarjeta De Credito', 'Tarjeta De Credito'),
    ('Tarjeta De Debito', 'Tarjeta De Debito'),
    ('Efectivo', 'Efectivo'),
]

class Nota(models.Model):
    no_trabajo = models.CharField(max_length=100, blank=True, null=True)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    entrega = models.CharField(max_length=50, choices=ENTREGA)
    pago = models.CharField(max_length=50, choices=PAGO)
    
    anticipo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    incluye_iva = models.BooleanField(default=False)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha = models.DateField(null=True, blank=True)
    
    contacto = models.CharField(max_length=100, blank=True)
    telefono = models.CharField(max_length=20, blank=True)
    
    factura = models.CharField(max_length=100, blank=True, null=True)
    no_factura = models.BooleanField(default=False)  # Checkbox para "no factura"
    
    # Campos calculados, no es necesario guardarlos en la DB salvo que quieras historial
    # total = models.DecimalField(max_digits=12, decimal_places=2, default=0)  # opcional

    def __str__(self):
        return f'Nota #{self.id} - {self.tipo}'

class ProductoNota(models.Model):
    nota = models.ForeignKey(Nota, on_delete=models.CASCADE, related_name='productos')
    nombre = models.TextField()
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)  # cantidad * precio
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)  # subtotal + iva si aplica

    def save(self, *args, **kwargs):
        # Calculamos subtotal y total antes de guardar
        self.subtotal = self.cantidad * self.precio
        # Si quieres calcular total con IVA aquí, pero normalmente el IVA se calcula a nivel Nota
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.nombre} ({self.cantidad} x {self.precio})'