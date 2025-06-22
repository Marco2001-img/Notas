from django.urls import path
from . import views

urlpatterns = [
    path('verClientes/', views.ver_clientes, name='misClientes'),
    path('AgregarCliente/', views.nuevo_clientes, name='AgregarsClientes'),
    path('ModificarCliente/<int:pk>/', views.modificar_cliente, name='ActualizarClientes'),
    path('EliminarCliente/<int:pk>/', views.eliminar_cliente, name='EliminarClientes'),
    path('clientes/pdf/', views.generar_pdf_clientes, name='clientes_pdf'),

]
