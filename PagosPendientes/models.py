from django.db import models


class Pago(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_pago = models.DateField()
    costo = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.titulo