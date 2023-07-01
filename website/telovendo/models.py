from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model


# Create your models here.

class Productos(models.Model):              # Modelo de productos
    nombre = models.CharField(max_length=45, null=False, blank=False)
    descripcion = models.CharField(max_length=45, null=False, blank=False)
    stock = models.IntegerField(null=False, blank=False)
    precio = models.IntegerField(null=False, blank=False)
    urlfoto = models.CharField(max_length=45, null=True, blank=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'


class Estado_Pedido(models.Model):          # Modelo de estados de pedidos
    estado = models.CharField(max_length=45, null=False, blank=False)

    def __str__(self):
        return self.estado

    class Meta:
        verbose_name = 'Estado de pedido'
        verbose_name_plural = "Estado de pedidos"


class MetodoPago(models.Model):             # Modelo de métodos de pago
    nombre = models.CharField(max_length=45, null=False, blank=False)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Medio de pago'
        verbose_name_plural = 'Medios de pago'


class Empresas(models.Model):               # Modelo de listado de empresas
    rut = models.CharField(max_length=12, null=False, blank=False)
    nombre_empresa = models.CharField(max_length=50, null=False, blank=False)

    def __str__(self):
        return self.nombre_empresa
    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'


# Clase para usuarios personalizados
class CustomUser(AbstractUser):             # Modelo para usuarios personalizados
    run = models.CharField(max_length=12, null=False, blank=False)
    idEmpresa = models.ForeignKey(Empresas, on_delete=models.DO_NOTHING, null=True, blank = True)
    group = models.CharField(max_length=45, null=True)

    def __str__(self):
        return self.username

class Direcciones(models.Model):            # Modelo de direcciones de empresas
    idEmpresa = models.ForeignKey(Empresas, on_delete=models.DO_NOTHING, null=False, blank=False)
    direccion = models.CharField(max_length=45, null=False, blank=False)
    numero = models.IntegerField(null=False, blank=False)
    Comuna = models.CharField(max_length=45, null=False, blank=False)
    descripcion = models.CharField(max_length=45, null=True, blank=True)

    def __str__(self):
        return self.direccion
    
    class Meta:
        verbose_name = 'Dirección'
        verbose_name_plural = 'Direcciones'


class Pedidos(models.Model):                # Modelo de pedidos
    fecha_creacion = models.DateTimeField(default=timezone.now)
    idMetodoPago = models.ForeignKey(MetodoPago, on_delete=models.DO_NOTHING, null=False, blank=False)
    idEstado = models.ForeignKey(Estado_Pedido, on_delete=models.DO_NOTHING, null=False, blank=False)
    idDireccion = models.ForeignKey(Direcciones, on_delete=models.DO_NOTHING, null=False, blank=False)
    idUsuario = models.ForeignKey(get_user_model(), on_delete=models.DO_NOTHING, null=True, blank=True)
    idEmpresa = models.ForeignKey(Empresas, on_delete=models.DO_NOTHING, null=True, blank=True)
    instrucciones_entrega = models.CharField(max_length=100, null=True, blank=True)
    total_pedido = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'


class Detalles_Pedido(models.Model):        # Modelo de detalle de pedido
    idProductos = models.ForeignKey(Productos, on_delete=models.DO_NOTHING, null=False, blank=False)
    idPedidos = models.ForeignKey(Pedidos, on_delete=models.DO_NOTHING, null=False, blank=False)
    cantidad = models.IntegerField(null=False, blank=False)
    precio = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Detalle de pedido'
        verbose_name_plural = 'Detalle de pedidos'


# class Users(models.Model):
#     user = models.OneToOneField(User, on_delete=models.DO_NOTHING, default = None)
#     idEmpresa = models.ForeignKey(Empresas, on_delete=models.DO_NOTHING, null=True)
#     group = models.CharField(max_length=45, null=True)

#     def __str__(self):
#         return self.user.username
