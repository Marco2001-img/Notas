from django.urls import path
from . import views

urlpatterns = [
    path('verNota/', views.verNotas, name='Ver_nota'),
    #path('AgregarNota/', views.AgregarNotas, name='agregar_nota'),
    path('guardar-nota/', views.agregar_nota, name='guardar_nota'),
    
    path('editar/<int:nota_id>/', views.editar_nota, name='editar_nota'),
    path('actualizar/<int:nota_id>/', views.actualizar_nota, name='actualizar_nota'),  # POST desde JS

    path('pdf/<int:nota_id>/', views.generar_pdf_nota, name='nota_pdf'),

    path('eliminar-producto/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
]
