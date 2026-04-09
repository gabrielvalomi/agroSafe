from django.urls import path
from .views import cadastrar_pessoa, login_pessoa, logout_pessoa

urlpatterns = [
    path('cadastrar/', cadastrar_pessoa, name='cadastrar_pessoa'),
    path('login/', login_pessoa, name='login_pessoa'),
    path('logout/', logout_pessoa, name='logout_pessoa'),
]
