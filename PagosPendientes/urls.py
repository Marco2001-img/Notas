from django.urls import path
from . import views

urlpatterns = [
    path('verPagos/', views.verPagos, name='ver_pago'),
    path('ActualizarPagos/', views.ModificarPagos, name='modificar_pago'),
]
