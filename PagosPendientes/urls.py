from django.urls import path
from . import views

urlpatterns = [
    path('verPagos/', views.verPagos, name='ver_pago'),
    path('modificarPago/<int:pago_id>/', views.modificarPago, name='modificar_pago'),
    path('eliminarPago/<int:pago_id>/', views.eliminarPago, name='eliminar_pago'),
    path('pagos/pdf/', views.generar_pdf_pagos, name='pagos_pdf'),
]
