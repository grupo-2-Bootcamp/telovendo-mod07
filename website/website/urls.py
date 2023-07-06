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
from mainsite.views import Index, CatalogoIndex, CatalogoList

# Vistas de la app principal
from telovendo.views import LoginView, InternoView, PedidosView, RegistroView, DetallesPedidosView, UpdateEstadoPedidoView, ProductosView, ProductoEditView, ProductoCreateView, ProductoDeleteView, AddPedidosPasoUnoView, AddPedidosPasoDosView, AddPedidosPasoTresView, CierrePedidoView

# from django.conf import settings
# from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Index.as_view(), name='index'),
    path('catalogo', CatalogoIndex.as_view(), name='catalogo'), 
    path('catalogo/categoria/<int:id_categoria>', CatalogoList.as_view(), name='categoria'),
    path('registrarse', RegistroView.as_view(), name='registrarse'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('internal/home', login_required(InternoView.as_view()), name='internal'),
    path('internal/pedidos', login_required(PedidosView.as_view()), name = 'pedidos'),
    path('internal/pedidos/orden/<int:idpedido>', login_required(DetallesPedidosView.as_view()), name='detalle_pedido'),
    path('internal/pedidos/orden/<int:idpedido>/modifica/estado', login_required(UpdateEstadoPedidoView.as_view()), name='modifica_estado_pedido'),
    path('internal/pedidos/agregar/paso-uno', login_required(AddPedidosPasoUnoView.as_view()), name='nuevo_pedido'),
    path('internal/pedidos/agregar/paso-dos', login_required(AddPedidosPasoDosView.as_view()), name='nuevo_pedido_paso_dos'),
    path('internal/pedidos/agregar/paso-tres', login_required(AddPedidosPasoTresView.as_view()), name='nuevo_pedido_paso_tres'),
    path('internal/productos/', login_required(ProductosView.as_view()), name='productos'),
    path('internal/productos/agregar/', login_required(ProductoCreateView.as_view()), name='agregar_producto'),
    path('internal/productos/<int:id_producto>/editar/', login_required(ProductoEditView.as_view()), name='editar_producto'),
    path('internal/productos/<int:pk>/eliminar/', login_required(ProductoDeleteView.as_view()), name='eliminar_producto'),
    path('internal/pedidos/cierre', login_required(CierrePedidoView.as_view()), name='cierre_pedidos')
]


# Configuración para servir archivos de medios en desarrollo
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)