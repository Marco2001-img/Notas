from django.urls import path
from . import views

urlpatterns = [
    path('verClientes/', views.ver_clientes, name='misClientes'),
    path('AgregarCliente/', views.nuevo_clientes, name='AgregarsClientes'),
    path('ModificarCliente/', views.modificar_cliente, name='ActualizarClientes'),
]
