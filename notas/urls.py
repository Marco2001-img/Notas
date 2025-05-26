from django.urls import path
from . import views

urlpatterns = [
    path('verNota/', views.verNotas, name='Ver_nota'),
    path('AgregarNota/', views.AgregarNotas, name='agregar_nota'),
    path('ModificarNota/', views.ModificarNotas, name='actualizar_nota'),
]
