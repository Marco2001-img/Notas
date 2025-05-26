from django.urls import path
from . import views

urlpatterns = [
    path('lista/', views.lista_empleados, name='lista_empleados'),
    path('nuevoEmpleado/', views.nuevo_empleados, name='nuevo_empleados'),
    path('modificarEmpleado/', views.modificar_empleados, name='modificar_empleados'),
]
