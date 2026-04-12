"""
URL configuration for agroSafe project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.shortcuts import redirect

def home(request):
    return render(request, 'main/login.html')


def cadastro_page(request):
    return render(request, 'main/cadastro.html')


def porteiro_page(request):
    pessoa_id = request.session.get('pessoa_id')
    if not pessoa_id:
        return redirect('/')

    nome = request.session.get('pessoa_nome', 'Usuário')
    return render(request, 'porteiro/inicio.html', {'nome': nome})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('appbk/', include('appbk.urls')),
    path('', home),
    path('cadastro/', cadastro_page),
    path('porteiro/', include('appbk.urls_porteiro')),
]
