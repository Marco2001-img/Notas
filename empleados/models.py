from django.db import models

# Create your models here.
# models.py
from django.db import models

class Empleado(models.Model):
    nombre = models.CharField(max_length=100)
    edad = models.PositiveIntegerField()
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    cargo = models.CharField(max_length=100)
    numero_cuenta = models.CharField(max_length=20)
    nombre_banco = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno}"
