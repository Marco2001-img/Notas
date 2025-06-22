from django.urls import path
from . import views

urlpatterns = [
    path('lista/', views.lista_empleados, name='lista_empleados'),
    path('nuevoEmpleado/', views.nuevo_empleados, name='nuevo_empleados'),
    path('modificarEmpleado/<int:id>/', views.modificar_empleados, name='modificar_empleados'),
    path('eliminarEmpleado/<int:id>/', views.eliminar_empleado, name='eliminar_empleado'),
     path('empleados/pdf/', views.generar_pdf_empleados, name='empleados_pdf'),
]
