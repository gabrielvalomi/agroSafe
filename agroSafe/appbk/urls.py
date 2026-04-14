from django.contrib import admin
from django.urls import path, include
from .views import cadastrar_granja, login_granja, logout_granja, editar_granja, deletar_granja, home, cadastro_page
from . import views_porteiro

urlpatterns = [
    path('admin/', admin.site.urls),

    # Main pages
    path('', home, name='home'),
    path('login/', home, name='login_page'),
    path('cadastro/', cadastro_page, name='cadastro'),

    # Granja API endpoints
    path('cadastrar/', cadastrar_granja, name='cadastrar_granja'),
    path('login/', login_granja, name='login_granja'),
    path('logout/', logout_granja, name='logout_granja'),
    path('granja/<int:id>/editar/', editar_granja, name='editar_granja'),
    path('granja/<int:id>/deletar/', deletar_granja, name='deletar_granja'),

    # Porteiro endpoints
    path('porteiro/', views_porteiro.inicio, name='porteiro_inicio'),
    path('porteiro/foto/', views_porteiro.foto, name='porteiro_foto'),
    path('porteiro/revisao/', views_porteiro.revisao, name='porteiro_revisao'),
]
