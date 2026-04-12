from django.urls import path
from .views import cadastrar_granja, login_granja, logout_granja

urlpatterns = [
    path('cadastrar/', cadastrar_granja, name='cadastrar_granja'),
    path('login/', login_granja, name='login_granja'),
    path('logout/', logout_granja, name='logout_granja'),
]
