from django.urls import path
from .views import cadastrar_pessoa

urlpatterns = [
    path('cadastrar/', cadastrar_pessoa, name='cadastrar_pessoa'),
]
