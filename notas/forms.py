from django import forms
from .models import Nota

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
    ('Tarjeta De Debito', 'arjeta De Debito'),
    ('Efectivo', 'Efectivo'),
]


class NotaForm(forms.ModelForm):
    class Meta:
        model = Nota
        fields = ['no_trabajo', 'contacto', 'telefono', 'fecha', 'tipo', 'entrega', 'pago', 'anticipo', 'incluye_iva','factura']
        widgets = {
            'no_trabajo': forms.TextInput(attrs={'class': 'form-control'}),
            'contacto': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'factura': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'tipo': forms.Select(choices=TIPO_CHOICES, attrs={'class': 'form-select'}),
            'entrega': forms.Select(choices=ENTREGA, attrs={'class': 'form-select'}),
            'pago': forms.Select(choices=PAGO, attrs={'class': 'form-select'}),
            'anticipo': forms.NumberInput(attrs={'class': 'form-control'}),
            'incluye_iva': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'checkDefault'}),
        }
        labels = {
            'no_trabajo': 'No. de Trabajo',
            'incluye_iva': 'IVA',
        }
