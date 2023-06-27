from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Productos(models.Model):
    nombre = models.CharField(max_length=45, null=False, blank=False)
    descripcion = models.CharField(max_length=45, null=False, blank=False)
    stock = models.IntegerField(null=False, blank=False)
    precio = models.IntegerField(null=False, blank=False)
    urlfoto = models.CharField(max_length=45, null=False, blank=False)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'


class Estado_Pedido(models.Model):
    estado = models.CharField(max_length=45, null=False, blank=False)

    def __str__(self):
        return self.estado

    class Meta:
        verbose_name = 'Estado de pedido'
        verbose_name_plural = "Estado de pedidos"


class MetodoPago(models.Model):
    nombre = models.CharField(max_length=45, null=False, blank=False)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Medio de pago'
        verbose_name_plural = 'Medios de pago'


class Empresas(models.Model):
    rut = models.CharField(max_length=10, null=False, blank=False)
    nombre_empresa = models.CharField(max_length=30, null=False, blank=False)

    def __str__(self):
        return self.nombre_empresa
    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'


class Users(models.Model):
    idEmpresa = models.ForeignKey(Empresas, on_delete=models.DO_NOTHING, null=True)
    username = models.CharField(max_length=30, null=False, blank=False)
    first_name = models.CharField(max_length=45, null=False, blank=False)
    last_name = models.CharField(max_length=45, null=False, blank=False)
    password = models.CharField(max_length=30, null=False, blank=False)
    group = models.CharField(max_length=45, null=True)

    def __str__(self):
        return self.username
    
class Direcciones(models.Model):
    idEmpresa = models.ForeignKey(Empresas, on_delete=models.DO_NOTHING, null=False, blank=False)
    direccion = models.CharField(max_length=45, null=False, blank=False)
    numero = models.IntegerField(null=False, blank=False)
    Comuna = models.CharField(max_length=45, null=False, blank=False)
    descripcion = models.CharField(max_length=45, null=True)

    def __str__(self):
        return self.direccion
    
    class Meta:
        verbose_name = 'Dirección'
        verbose_name_plural = 'Direcciones'


class Pedidos(models.Model):
    fecha_creacion = models.DateTimeField(default=timezone.now)
    idMetodoPago = models.ForeignKey(MetodoPago, on_delete=models.DO_NOTHING, null=False, blank=False)
    idEstado = models.ForeignKey(Estado_Pedido, on_delete=models.DO_NOTHING, null=False, blank=False)
    idDireccion = models.ForeignKey(Direcciones, on_delete=models.DO_NOTHING, null=False, blank=False)
    idUsuario = models.ForeignKey(Users, on_delete=models.DO_NOTHING, null=True)
    idEmpresa = models.ForeignKey(Empresas, on_delete=models.DO_NOTHING, null=True)
    total_pedido = models.IntegerField(null=False, blank=False)

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'


class Detalles_Pedido(models.Model):
    idProductos = models.ForeignKey(Productos, on_delete=models.DO_NOTHING, null=False, blank=False)
    idPedidos = models.ForeignKey(Pedidos, on_delete=models.DO_NOTHING, null=False, blank=False)
    cantidad = models.IntegerField(null=False, blank=False)
    precio = models.IntegerField(null=False, blank=False)