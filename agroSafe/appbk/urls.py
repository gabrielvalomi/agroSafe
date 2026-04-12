from django.urls import path
from .views import cadastrar_granja, login_granja, logout_granja, editar_granja, deletar_granja

urlpatterns = [
    path('cadastrar/', cadastrar_granja, name='cadastrar_granja'),
    path('login/', login_granja, name='login_granja'),
    path('logout/', logout_granja, name='logout_granja'),
    path('granja/<int:id>/editar/', editar_granja, name='editar_granja'),
    path('granja/<int:id>/deletar/', deletar_granja, name='deletar_granja'),
]
