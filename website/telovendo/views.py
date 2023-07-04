import os
import random
import string
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView, DeleteView
from django.db.models import F, Sum
from telovendo.form import FormularioLogin, FormularioRegistro, FormularioUpdateEstado,FormularioProductos, FormularioEditarProductos, FormularioPedidos, FormularioDetalle
from telovendo.models import Pedidos, CustomUser, Empresas, Direcciones, Detalles_Pedido, Estado_Pedido, Productos
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.urls import reverse
from django.contrib import messages

# Genera contraseñas aleatorias
def generate_random_password():
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(6))
    return password

# Create your views here.

class LoginView(TemplateView):              # Vista de acceso al sistema interno
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        formulario = FormularioLogin()
        title = 'Acceso al sitio interno'
        return render(request, self.template_name, {'formulario': formulario, 'title': title})

    def post(self, request, *args, **kwargs):
        title = 'Acceso al sitio interno'
        form = FormularioLogin(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = CustomUser.objects.filter(email=email).first()
            if user is not None:
                if user.is_active:
                    authenticated_user = authenticate(request, username=user.username, password=password)
                    login(request, authenticated_user)
                    return redirect('internal')
            form.add_error('email', 'Se han ingresado las credenciales equivocadas.')
        return render(request, self.template_name, {'form': form, 'title': title})

class InternoView(TemplateView):            # Vista de pagina principal interna
    template_name = 'internal.html'
    def get(self, request, *args, **kwargs):
        context = {
            'title': 'Bienvenido al sistema interno de TeLoVendo',
        }
        return render(request, self.template_name, context)
    

class PedidosView(TemplateView):            # Vista de pedidos
    template_name = 'pedidos.html'

    def get(self, request, *args, **kwargs):
        context ={
            'title': 'Gestión de pedidos',
            'pedidos': Pedidos.objects.all().order_by('id'),
        }
        return render(request,self.template_name, context)


class DetallesPedidosView(TemplateView):            # Vista de pagina detalles pedidos
    template_name = 'detalles_pedidos.html'
    def get(self, request, idpedido, *args, **kwargs):
        try:
            pedido = Pedidos.objects.get(id=idpedido)
        except Pedidos.DoesNotExist:
            return render(request, 'elemento_no_existe.html')
        context ={
            'title': f'Detalle de orden {pedido}',
            'pedido': pedido,
            'empresa': Empresas.objects.get(id=pedido.idEmpresa_id),
            'direccion': Direcciones.objects.get(id=pedido.idDireccion_id),
            'detalle_pedido': Detalles_Pedido.objects.filter(idPedidos=idpedido).annotate(total=F('cantidad') * F('precio')),
            'usuario': CustomUser.objects.get(id=pedido.idUsuario_id),
            'total_pedido': Detalles_Pedido.objects.filter(idPedidos=idpedido).aggregate(total=Sum(F('cantidad') * F('precio')))['total'],
            }
        return render(request, self.template_name, context)

class UpdateEstadoPedidoView(TemplateView):
    template_name = 'modifica_estado.html'
    
    def get(self, request, *args, **kwargs):
        idpedido = kwargs['idpedido']
        try:
            pedido = Pedidos.objects.get(id=idpedido)
        except Pedidos.DoesNotExist:
            return render(request, 'elemento_no_existe.html')
        context = {
            'form': FormularioUpdateEstado(instance=pedido),
            'idpedido': idpedido,
            'pedido': Pedidos.objects.get(id=idpedido),
            'title': f'Modificar el estado del pedido {idpedido}',
        }
        return render(request, self.template_name, context)

    def post(self, request, idpedido, *args, **kwargs):
        instance = get_object_or_404(Pedidos, id=self.kwargs['idpedido'])
        form = FormularioUpdateEstado(request.POST, instance=instance)
        reenvio = reverse('detalle_pedido', kwargs={'idpedido': idpedido})
        if form.is_valid():
            form.save()
            return redirect(reenvio)
        return self.render_to_response(self.get_context_data())


class RegistroView(TemplateView):
    template_name = 'registro.html'

    def get(self, request, *args, **kwargs):
        context = {
            'formulario': FormularioRegistro(),
            'title': 'Registro de Usuario',
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = FormularioRegistro(request.POST, request.FILES)
        title = 'Registro de Usuarios'
        if form.is_valid():
            username = form.cleaned_data['username']
            password = generate_random_password()
            user = form.save(commit=False)
            user.set_password(password)
            user.save()
            group = form.cleaned_data['group']
            if group:
                group.user_set.add(user)
            mensajes = {'enviado': True, 'resultado': 'Has creado un nuevo usuario exitosamente'}
            correo_destino = form.cleaned_data['email']
            mensaje = f'''
                Bienvenido a Telovendo.
                Gracias por registrarte en nuestro sitio web. A continuación se le adjunta su contraseña de acceso
                contraseña :   {password} 
                Muchas Gracias por su preferencia
            '''
            send_mail(
                '[TE LO VENDO] - Contraseña',
                mensaje,
                os.environ.get('EMAIL_HOST_USER'),  # Usar el correo configurado en settings.py
                [correo_destino],  # Enviar el correo al destinatario ingresado por el usuario
                fail_silently=False
            )
            messages.success(request, mensajes['resultado'])  # Almacenar el mensaje de éxito
            return redirect('login')  # Redirigir al formulario de inicio de sesión

        mensajes = {'enviado': False, 'resultado': form.errors}
        context = {
            'formulario': form,
            'mensajes': mensajes,
            'title': title
        }
        return render(request, self.template_name, context)

class ProductosView(TemplateView):              #Vista del Registro de Productos
    template_name = 'productos.html'

    def get(self, request, *args, **kwargs):
        context = {
            'title': 'Gestión de Productos',
            'productos': Productos.objects.all().order_by('id'),
        }
        return render(request, self.template_name, context)

class ProductoCreateView(TemplateView): 
    template_name = 'agregar_producto.html'
    def get(self, request, *args, **kwargs):

        context = {
            'title': 'Crear nuevo Producto',
            'form': FormularioProductos(),
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = FormularioProductos(request.POST, request.FILES)
        if form.is_valid():
            registro = Productos(
                nombre= form.cleaned_data['nombre'],
                descripcion= form.cleaned_data['descripcion'],
                precio= form.cleaned_data['precio'],
                stock= form.cleaned_data['stock'],
            )
            registro.save()
            mensajes = {'enviado': True, 'resultado': 'Has creado un nuevo producto exitosamente'}
            return redirect('productos')
        else:
            mensajes = {'enviado': False, 'resultado': form.errors}
        context = {
            'title': 'Crear nuevo Producto',
            'mensajes': mensajes,
            'form': form
        }
        return render(request, self.template_name, context)


class ProductoEditView(TemplateView):
    template_name = 'editar_producto.html'

    def get(self, request, *args, **kwargs):
        id_producto = kwargs['id_producto']
        try:
            producto = Productos.objects.get(id=id_producto)
        except Productos.DoesNotExist:
            return render(request, 'elemento_no_existe.html')
        form = FormularioEditarProductos(instance=producto)
        context = {
            'form': form,
            'id_producto': id_producto,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        id_producto = kwargs['id_producto']
        producto = Productos.objects.get(id=id_producto)
        form = FormularioEditarProductos(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            mensajes = {'enviado': True, 'resultado': 'Has actualizado el producto exitosamente'}
            return redirect('productos') 
        else:
            mensajes = {'enviado': False, 'resultado': form.errors}
        context = {
            'form': form,
            'id_producto': id_producto,
            'mensajes': mensajes
        }
        return render(request, self.template_name, context)
    
class ProductoDeleteView(DeleteView):
    model = Productos
    template_name = 'eliminar_producto.html'
    def get(self, request, *args, **kwargs):
        context = {
            'title': 'Eliminar Producto',
        }
        return render(request, self.template_name, context)
    
    def get_success_url(self):
        return reverse('productos')
    

class AddPedidosView(TemplateView):
    template_name = 'agregar_pedido.html'

    def get(self, request, *args, **kwargs):
        context ={
            'title': 'Crear nuevo pedido',
            'form': FormularioPedidos()
        }
        return render(request,self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = FormularioPedidos(request.POST)
        if form.is_valid():
            registro = Pedidos(
                idEmpresa = form.cleaned_data['idEmpresa'],
                idDireccion = form.cleaned_data['idDireccion'],
                instrucciones_entrega = form.cleaned_data['instrucciones_entrega'],
                idUsuario = CustomUser.objects.get(id=request.user.id),
                idEstado = Estado_Pedido.objects.get(id=1),
                idMetodoPago = form.cleaned_data['idMetodoPago'],
            )
            registro.save()
            mensajes = {'enviado': True, 'resultado': 'Has creado un nuevo producto exitosamente'}
            return redirect('nuevo_pedido_paso_dos')
        else:
            mensajes = {'enviado': False, 'resultado': form.errors}

        context = {
            'form': form,
            'mensajes': mensajes,
            }
        return render(request, self.template_name, context)
    
class AddPedidosPasoDosView(TemplateView):
    template_name = 'agregar_pedido_paso_dos.html'

    def get(self, request, *args, **kwargs):
        last_pedido = Pedidos.objects.filter(idUsuario=request.user).latest('id')
        context ={
            'title': 'Segundo paso',
            'last_pedido': last_pedido,
            'form': FormularioDetalle(),
            'detalle_pedido' : Detalles_Pedido.objects.filter(idPedidos=last_pedido),
        }
        return render(request,self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = FormularioDetalle(request.POST)
        if form.is_valid():
            producto = form.cleaned_data.get('idProductos')
            registro = Detalles_Pedido(
                cantidad = form.cleaned_data['cantidad'],
                idPedidos = Pedidos.objects.filter(idUsuario=request.user).latest('id'),
                idProductos = form.cleaned_data['idProductos'],
                precio = Productos.objects.get(nombre=producto).precio,
            )
            registro.save()
            mensajes = {'enviado': True, 'resultado': 'Has agregado un nuevo elemento al pedido exitosamente'}
            return redirect('nuevo_pedido_paso_dos')
        else:
            mensajes = {'enviado': False, 'resultado': form.errors}

        context = {
            'form': form
        }
        return render(request, self.template_name, context)
    