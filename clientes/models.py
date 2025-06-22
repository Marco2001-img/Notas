from django.db import models

# models.py
from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    rfc = models.CharField(max_length=13)
    domicilio = models.CharField(max_length=200)
    calle = models.CharField(max_length=100)
    detalles = models.CharField(max_length=200, blank=True)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

