import os
import random
import string
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView, DeleteView
from telovendo.form import FormularioLogin, FormularioRegistro, FormularioUpdateEstado,FormularioProductos, FormularioEditarProductos
from telovendo.models import Pedidos, CustomUser, Empresas, Direcciones, Detalles_Pedido, Estado_Pedido, Productos
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.urls import reverse

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
        title = 'Bienvenido al sistema interno de TeLoVendo'
        return render(request, self.template_name, {'title': title,})
    

class PedidosView(TemplateView):            # Vista de pedidos
    template_name = 'pedidos.html'

    def get(self, request, *args, **kwargs):
        title = 'Gestión de pedidos'
        pedidos = Pedidos.objects.all().order_by('id')
        context ={
            'title':title,
            'pedidos': pedidos
        }
        return render(request,self.template_name, context)

class DetallesPedidosView(TemplateView):            # Vista de pagina detalles pedidos
    template_name = 'detalles_pedidos.html'
    def get(self, request, idpedido, *args, **kwargs):
        try:
            pedido = Pedidos.objects.get(id=idpedido)
        except Pedidos.DoesNotExist:
            return render(request, 'elemento_no_existe.html')
        empresa = Empresas.objects.get(id=pedido.idEmpresa_id)
        usuario = CustomUser.objects.get(id=pedido.idUsuario_id)
        direccion = Direcciones.objects.get(id=pedido.idDireccion_id)
        detalle_pedido = Detalles_Pedido.objects.filter(idPedidos=idpedido)
        context ={
            'title': f'Detalle de orden {pedido}',
            'pedido': pedido,
            'empresa': empresa,
            'direccion': direccion,
            'detalle_pedido': detalle_pedido,
            'usuario': usuario,
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
        volver_atras = reverse('detalle_pedido', kwargs={'idpedido': idpedido})
        context = {
            'form': FormularioUpdateEstado(instance=pedido),
            'idpedido': idpedido,
            'pedido': Pedidos.objects.get(id=idpedido),
            'title': f'Modificar el estado del pedido {idpedido}',
            'volver_atras': volver_atras,
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
        form = FormularioRegistro()
        title = 'Registro de Usuario'
        context = {
            'formulario': form,
            'title': title
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
        else:
            mensajes = {'enviado': False, 'resultado': form.errors}
        correo_destino = form.cleaned_data['email']
        context = {
            'formulario': form,
            'mensajes': mensajes,
            'title': title
        }

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

        return render(request, self.template_name, context), redirect('login')

class ProductosView(TemplateView):              #Vista del Registro de Productos
    template_name = 'productos.html'

    def get(self, request, *args, **kwargs):
        title = 'Gestión de Productos'
        productos = Productos.objects.all().order_by('id')
        context = {
            'title': title,
            'productos': productos,
        }
        return render(request, self.template_name, context)

class ProductoCreateView(TemplateView): 
    template_name = 'agregar_producto.html'
    def get(self, request, *args, **kwargs):
        title = 'Crear nuevo Producto'
        form = FormularioProductos()
        context = {
            'title': title,
            'form': form
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = FormularioProductos(request.POST, request.FILES)
        title = 'Gestión de Productos'
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            descripcion = form.cleaned_data['descripcion']
            precio = form.cleaned_data['precio']
            stock = form.cleaned_data['stock']
            registro = Productos(
                nombre=nombre,
                descripcion=descripcion,
                precio=precio,
                stock=stock
            )
            registro.save()
            mensajes = {'enviado': True, 'resultado': 'Has creado un nuevo producto exitosamente'}
            return redirect('productos')
        else:
            mensajes = {'enviado': False, 'resultado': form.errors}

        context = {
            'title': title,
            'mensajes': mensajes,
            'form': form
        }
        return render(request, self.template_name, context)


class ProductoEditView(TemplateView):
    template_name = 'editar_producto.html'

    def get(self, request, *args, **kwargs):
        title = 'Editar datos del Producto'
        id_producto = kwargs['id_producto']
        try:
            producto = Productos.objects.get(id=id_producto)
        except Productos.DoesNotExist:
            return render(request, 'elemento_no_existe.html')
        form = FormularioEditarProductos(instance=producto)
        context = {
            'form': form,
            'id_producto': id_producto,
            'title': title
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
        title = 'Eliminar Producto'
        context = {
            'title': title
        }
        return render(request, self.template_name, context)
    
    def get_success_url(self):
        return reverse('productos')