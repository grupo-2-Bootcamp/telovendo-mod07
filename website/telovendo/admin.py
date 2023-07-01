from django.contrib import admin
from telovendo.models import Estado_Pedido, MetodoPago, Empresas, Productos, Pedidos, Direcciones, CustomUser, Detalles_Pedido
from telovendo.form import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class CustomUserAdmin(UserAdmin):                   # Modelo de usuarios personalizados
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        'id',
        'email',
        'username',
        'first_name',
        'last_name',
        'run',
        'idEmpresa',
        'is_staff',
        ]
    ordering = ['id']
    fieldsets = UserAdmin.fieldsets + ((None, {'fields': ('run', 'idEmpresa')}),)         # Edición de usuarios en la administración
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {'fields': ('run','idEmpresa')}),)  # Creación de usuarios en la administración

admin.site.register(CustomUser, CustomUserAdmin)


# Modelos tablas auxiliares

class Estado_Pedido_Admin(admin.ModelAdmin):        # Modelo de Estado de pedidos
    list_display = ['id', 'estado']
    search_fields = ['estado']
    ordering = ['id']
    fields = ['estado']

admin.site.register(Estado_Pedido, Estado_Pedido_Admin)


class MetodoPago_Admin(admin.ModelAdmin):           # Modelo de Métodos de pago
    list_display = ['id', 'nombre']
    search_fields = ['nombre']
    ordering = ['id']
    fields = ['nombre']

admin.site.register(MetodoPago, MetodoPago_Admin)


class Empresas_Admin(admin.ModelAdmin):             # Modelo de empresas
    list_display = ['id', 'rut', 'nombre_empresa']
    search_fields = ['rut', 'nombre_empresa']
    ordering = ['id']
    fields = ['rut', 'nombre_empresa']

admin.site.register(Empresas, Empresas_Admin)


class Productos_Admin(admin.ModelAdmin):            # Modelo de Productos
    list_display = ['id', 'nombre', 'descripcion', 'stock', 'precio', 'urlfoto']
    list_filter = ['nombre', 'precio']
    search_fields = ['nombre']
    ordering = ['id']
    fields = ['nombre', 'descripcion', 'stock', 'precio', 'urlfoto']

admin.site.register(Productos, Productos_Admin)


class Pedidos_Admin(admin.ModelAdmin):              # Modelo de Pedidos
    list_display = ['id', 'fecha_creacion', 'idMetodoPago', 'idEstado', 'idDireccion', 'idUsuario', 'idEmpresa']
    list_filter = ['fecha_creacion', 'idEstado', 'idUsuario', 'idEmpresa']
    search_fields = ['fecha_creacion', 'idEstado', 'idUsuario', 'idEmpresa']
    ordering = ['id']
    fields = ['fecha_creacion', 'idMetodoPago', 'idEstado', 'idDireccion', 'instrucciones_entrega', 'idUsuario', 'idEmpresa', 'total_pedido']

admin.site.register(Pedidos, Pedidos_Admin)


class Direcciones_Admin(admin.ModelAdmin):          # Modelo de direcciones de empresas
    list_display = ['id', 'idEmpresa', 'direccion', 'numero', 'Comuna']
    list_filter = ['idEmpresa', 'Comuna']
    search_fields = ['idEmpresa', 'Comuna']
    ordering = ['id']
    fields = ['idEmpresa', 'direccion', 'numero', 'Comuna', 'descripcion']

admin.site.register(Direcciones, Direcciones_Admin)


class DetallePedidos_Admin(admin.ModelAdmin):       # Modelo de detalles de pedido
    list_display = ['id', 'idPedidos', 'idProductos', 'cantidad', 'precio' ]
    list_filter = ['idPedidos']
    search_fields = ['idPedidos']
    ordering = ['id']
    fields = ['idPedidos', 'idProductos', 'cantidad', 'precio' ]

admin.site.register(Detalles_Pedido, DetallePedidos_Admin)