'''
URL configuration for website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
'''
# Funciones de Django
from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required

# Vistas de paginas principales
from mainsite.views import Index

# Vistas de la app principal
from telovendo.views import LoginView, InternoView, PedidosView, RegistroView, DetallesPedidosView, UpdateEstadoPedidoView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('internal/home', login_required(InternoView.as_view()), name='internal'),
    path('internal/pedidos', login_required(PedidosView.as_view()), name = 'pedidos'),
    path('internal/pedidos/orden/<int:idpedido>', login_required(DetallesPedidosView.as_view()), name='detalle_pedido'),
    path('internal/pedidos/orden/<int:idpedido>/modifica/estado', login_required(UpdateEstadoPedidoView.as_view()), name='modifica_estado_pedido'),
    path('registrarse', RegistroView.as_view(), name='registrarse'),
]
