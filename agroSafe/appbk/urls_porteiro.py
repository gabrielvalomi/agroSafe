from django.urls import path

from . import views_porteiro

urlpatterns = [
	path('', views_porteiro.inicio, name='porteiro_inicio'),
	path('foto/', views_porteiro.foto, name='porteiro_foto'),
	path('revisao/', views_porteiro.revisao, name='porteiro_revisao'),
]
