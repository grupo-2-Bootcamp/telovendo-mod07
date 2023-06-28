from django.contrib import admin
from telovendo.models import Estado_Pedido, MetodoPago, Empresas, Productos, Pedidos, Direcciones, Detalles_Pedido, CustomUser
from telovendo.form import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
# from telovendo.models import Estado_Pedido, MetodoPago, Empresas, Productos, Pedidos, Direcciones, Detalles_Pedido,Users

# Register your models here.

# Modelo de usuarios

class CustomUserAdmin(UserAdmin):
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
        'group',
        'is_staff',
        ]
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("run", "idEmpresa")}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("run",)}),)

admin.site.register(CustomUser, CustomUserAdmin)

# Modelos tablas auxiliares

class Estado_Pedido_Admin(admin.ModelAdmin):
    list_display = ['id', 'estado']
    search_fields = ['estado']
    ordering = ['estado']
    fields = ['estado']

admin.site.register(Estado_Pedido, Estado_Pedido_Admin)


class MetodoPago_Admin(admin.ModelAdmin):
    list_display = ['id', 'nombre']
    search_fields = ['nombre']
    ordering = ['nombre']
    fields = ['nombre']

admin.site.register(MetodoPago, MetodoPago_Admin)


class Empresas_Admin(admin.ModelAdmin):
    list_display = ['id', 'rut', 'nombre_empresa']
    search_fields = ['rut', 'nombre_empresa']
    ordering = ['rut', 'nombre_empresa']
    fields = ['rut', 'nombre_empresa']

admin.site.register(Empresas, Empresas_Admin)


class Productos_Admin(admin.ModelAdmin):
    list_display = ['id', 'nombre', 'descripcion', 'stock', 'precio', 'urlfoto']
    list_filter = ['nombre', 'precio']
    search_fields = ['nombre']
    ordering = ['nombre', 'precio']
    fields = ['nombre', 'descripcion', 'stock', 'precio', 'urlfoto']

admin.site.register(Productos, Productos_Admin)


class Pedidos_Admin(admin.ModelAdmin):
    list_display = ['id', 'fecha_creacion', 'idMetodoPago', 'idEstado', 'idDireccion', 'idUsuario', 'idEmpresa']
    list_filter = ['fecha_creacion', 'idEstado', 'idUsuario', 'idEmpresa']
    search_fields = ['fecha_creacion', 'idEstado', 'idUsuario', 'idEmpresa']
    ordering = ['fecha_creacion', 'idEstado']
    fields = ['fecha_creacion', 'idMetodoPago', 'idEstado', 'idDireccion', 'idUsuario', 'idEmpresa','total_pedido']

admin.site.register(Pedidos, Pedidos_Admin)


class Direcciones_Admin(admin.ModelAdmin):
    list_display = ['id', 'idEmpresa', 'direccion', 'numero', 'Comuna']
    list_filter = ['idEmpresa', 'Comuna']
    search_fields = ['idEmpresa', 'Comuna']
    ordering = ['idEmpresa', 'Comuna']
    fields = ['idEmpresa', 'direccion', 'numero', 'Comuna', 'descripcion']

admin.site.register(Direcciones, Direcciones_Admin)



