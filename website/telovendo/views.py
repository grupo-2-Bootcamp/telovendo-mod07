import os
import random
import string
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView, DeleteView
from django.db.models import F, Sum
from telovendo.form import FormularioLogin, FormularioRegistro, FormularioUpdateEstado,FormularioProductos, FormularioEditarProductos, FormularioPedidos, FormularioDetalle, FormularioSeleccionaEmpresa
from telovendo.models import Pedidos, CustomUser, Empresas, Direcciones, Detalles_Pedido, Estado_Pedido, Productos, MetodoPago
from django.core.mail import send_mail
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.files.base import ContentFile


# Genera contraseñas aleatorias
def generate_random_password():
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(6))
    return password

# Create your views here.

class LoginView(TemplateView):                                                              # Vista de acceso al sistema interno
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        formulario = FormularioLogin()
        title = 'Acceso al sitio interno'
        mensajes = request.session.get('mensajes', None)
        request.session.pop('mensajes', None)
        return render(request, self.template_name, {'formulario': formulario, 'title': title, 'mensajes': mensajes,})

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
    

class RegistroView(TemplateView):                                                           # Crea usuarios
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
            # mensajes = {'enviado': True, 'resultado': 'Has creado un nuevo usuario exitosamente'}
            request.session['mensajes'] = {'enviado': True, 'resultado': 'El usuario ha sido creado, tus datos de identificación se enviarán por email'}
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
            # messages.success(request, mensajes['resultado'])  # Almacenar el mensaje de éxito
            
            
            return redirect('login')  # Redirigir al formulario de inicio de sesión
        mensajes = {'enviado': False, 'resultado': form.errors}
        context = {
            'formulario': form,
            'mensajes': mensajes,
            'title': title
        }
        return render(request, self.template_name, context)

class InternoView(TemplateView):                                                            # Vista de pagina principal interna
    template_name = 'internal.html'
    def get(self, request, *args, **kwargs):
        primer_nombre = request.user.first_name
        apellido = request.user.last_name
        context = {
            'title': 'Bienvenido al sistema interno de TeLoVendo',
            'primer_nombre': primer_nombre,
            'apellido': apellido
        }
        return render(request, self.template_name, context)


class PedidosView(TemplateView):                                                            # Vista de todos los pedidos
    template_name = 'pedidos.html'
    def get(self, request, *args, **kwargs):
        request.session.pop('mensajes', None)
        if request.user.groups.first().id == 1:
            pedidos = Pedidos.objects.filter(idEmpresa_id=request.user.idEmpresa_id).order_by('id').filter(idUsuario_id=request.user.id)
        else:
            pedidos = Pedidos.objects.all()
        context ={
            'title': 'Gestión de pedidos',
            'pedidos': pedidos
        }
        return render(request,self.template_name, context)


class DetallesPedidosView(TemplateView):                                                    # Listado de detalles de un pedido
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
            'grupo_usuario_actual': request.user.groups.first().id,
            'total_pedido': Detalles_Pedido.objects.filter(idPedidos=idpedido).aggregate(total=Sum(F('cantidad') * F('precio')))['total'],
            'mensajes' : request.session.get('mensajes', None),
            }
        request.session.pop('mensajes', None)
        return render(request, self.template_name, context)

class UpdateEstadoPedidoView(TemplateView):                                                 # Actualiza el estado de los pedidos
    template_name = 'modifica_estado.html'
    
    def get(self, request, *args, **kwargs):
        idpedido = kwargs['idpedido']
        try:
            pedido = Pedidos.objects.get(id=idpedido)
        except Pedidos.DoesNotExist:
            return render(request, 'elemento_no_existe.html')
        pedido = Pedidos.objects.get(id=idpedido)
        email_cliente =  CustomUser.objects.get(id=pedido.idUsuario_id).email
        grupo_cliente = CustomUser.objects.get(id=pedido.idUsuario_id).groups.first().id
        context = {
            'form': FormularioUpdateEstado(instance=pedido),
            'idpedido': idpedido,
            'pedido': pedido,
            'title': f'Modificar el estado del pedido {idpedido}',
            'email_cliente': email_cliente,
            'grupo_cliente': grupo_cliente,
            'grupo_usuario': request.user.groups.first().id,
        }
        
        request.session['email_cliente'] = email_cliente
        request.session['grupo_cliente'] = grupo_cliente
        return render(request, self.template_name, context)

    def post(self, request, idpedido, *args, **kwargs):             
        instance = get_object_or_404(Pedidos, id=self.kwargs['idpedido'])
        form = FormularioUpdateEstado(request.POST, instance=instance)
        reenvio = reverse('detalle_pedido', kwargs={'idpedido': idpedido})
        pedido = self.kwargs['idpedido']
        email_cliente = request.session['email_cliente']
        grupo_cliente = request.session['grupo_cliente']
        request.session.pop('email_cliente', None)
        request.session.pop('grupo_cliente', None)
        if form.is_valid():
            form.save()
            request.session['mensajes'] = {'enviado': True, 'resultado': 'Se ha actualizado el estado del pedido'}
            estado = Pedidos.objects.get(id=pedido).idEstado
            if grupo_cliente == 1:
                mensaje = f'''
                    Cambio de estado de pedido.
                    El estado del pedido {pedido} ha cambiado, y su nuevo estado es {estado}
                    En caso de dudas, puede contactanos para revisar nuevamente su pedido.


                    Muchas Gracias por su preferencia
                '''
                send_mail(
                    f'[TeLoVendo] - Cambio de estado de pedido número {pedido}',
                    mensaje,
                    os.environ.get('EMAIL_HOST_USER'),  # Usar el correo configurado en settings.py
                    [email_cliente],  # Enviar el correo al destinatario ingresado por el usuario
                    fail_silently=False
                )
                request.session['mensajes'] = {'enviado': True, 'resultado': 'Se ha actualizado el estado del pedido y envíado un email al cliente'}
            return redirect(reenvio)
        return self.render_to_response(self.get_context_data())

class ProductosView(PermissionRequiredMixin, TemplateView):                                 # Lista los productos
    template_name = 'productos.html'
    permission_required = "telovendo.permiso_trabajadores"
    def get(self, request, *args, **kwargs):
        context = {
            'title': 'Gestión de Productos',
            'productos': Productos.objects.all().order_by('id'),
            'mensajes' : request.session.get('mensajes', None),
        }
        request.session.pop('mensajes', None)
        return render(request, self.template_name, context)

class ProductoCreateView(PermissionRequiredMixin, TemplateView):                            # Crea producto
    template_name = 'agregar_producto.html'
    permission_required = "telovendo.permiso_trabajadores"
    def get(self, request, *args, **kwargs):

        context = {
            'title': 'Crear nuevo Producto',
            'form': FormularioProductos(),
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        form = FormularioProductos(request.POST, request.FILES)
        if form.is_valid():
            if 'image' in request.FILES:
                image = request.FILES.get('image')
            else:
                image = form.ruta_fotoPerfil()

            registro = Productos(
                nombre= form.cleaned_data['nombre'],
                descripcion= form.cleaned_data['descripcion'],
                precio= form.cleaned_data['precio'],
                stock= form.cleaned_data['stock'],
                categoria = form.cleaned_data['idCategoria'],
                image = image
            )
            registro.save()
            request.session['mensajes'] = {'enviado': True, 'resultado': 'Has creado el producto exitosamente'}
            return redirect('productos')
        else:
            mensajes = {'enviado': False, 'resultado': form.errors}
        context = {
            'title': 'Crear nuevo Producto',
            'mensajes': mensajes,
            'form': form
        }
        return render(request, self.template_name, context)


class ProductoEditView(PermissionRequiredMixin, TemplateView):                              # Edición de productos
    template_name = 'editar_producto.html'
    permission_required = "telovendo.permiso_trabajadores"

    def get(self, request, *args, **kwargs):
        id_producto = kwargs['id_producto']
        try:
            producto = Productos.objects.get(id=id_producto)
        except Productos.DoesNotExist:
            return render(request, 'elemento_no_existe.html')
        form = FormularioEditarProductos(instance=producto)
        context = {
            'title': 'Editar producto',
            'form': form,
            'id_producto': id_producto,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        id_producto = kwargs['id_producto']
        try:
            producto = Productos.objects.get(id=id_producto)
        except Productos.DoesNotExist:
            return render(request, 'elemento_no_existe.html')
        form = FormularioEditarProductos(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            # Opcional: Puedes realizar acciones adicionales después de guardar la actualización
            request.session['mensajes'] = {'enviado': True, 'resultado': 'Has actualizado el producto exitosamente'}
            return redirect('productos')
        else:
            context = {
                'title': 'Editar producto',
                'form': form,
                'id_producto': id_producto,
            }
            return render(request, self.template_name, context)
    
class ProductoDeleteView(PermissionRequiredMixin, DeleteView):                              # Elimina productos
    model = Productos
    permission_required = "telovendo.permiso_trabajadores"
    template_name = 'eliminar_producto.html'
    
    def get_success_url(self):
        return reverse('productos')
    

class AddPedidosPasoUnoView(TemplateView):                                                  # Agrega pedidos
    template_name  = 'agregar_pedido_paso_uno.html'
    def get(self, request, *args, **kwargs):
        
        if request.user.groups.first().id == 1:
            empresas = Empresas.objects.filter(id=request.user.idEmpresa_id)
        else:
            empresas = Empresas.objects.all()
        context = {
            'title': '1/3 - Crear pedido',
            'form': FormularioSeleccionaEmpresa(),
            'usuario': request.user.groups.first().id,
            'empresa': empresas
        }
        request.session.pop('idEmpresa', None)
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        idEmpresa = request.POST.get('idEmpresa')
        request.session['idEmpresa'] = idEmpresa
        request.session['mensajes'] = {'enviado': True, 'resultado': 'Se ha seleccionado una empresa, ahora hay que completar algunos datos'}
        return redirect('nuevo_pedido_paso_dos')

class AddPedidosPasoDosView(TemplateView):                                                  # Agrega pedidos - paso 2
    template_name = 'agregar_pedido_paso_dos.html'

    def get(self, request, *args, **kwargs):
        mensajes = request.session.get('mensajes', None)
        empresa = request.session.get('idEmpresa', None)
        idempresa = Empresas.objects.get(id=empresa)
        direcciones = Direcciones.objects.filter(idEmpresa=empresa)
        metodospago = MetodoPago.objects.all().order_by('id')
        context ={
            'title': '2/3 - Seleccionar los datos de despacho',
            'form': FormularioPedidos(),
            'mensajes': mensajes,
            'empresa': empresa,
            'buscaempresa': idempresa,
            'direcciones': direcciones,
            'metodospago': metodospago,
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
            request.session['mensajes'] = {'enviado': True, 'resultado': 'Se ha creado el pedido exitosamente, ahora puedes llenar el pedido con los productos de la plataforma'}
            return redirect('nuevo_pedido_paso_tres')
        else:
            mensajes = {'enviado': False, 'resultado': form.errors}

        context = {
            'form': form,
            'mensajes': mensajes,
            }
        return render(request, self.template_name, context)
    
class AddPedidosPasoTresView(TemplateView):                                                 # Agrega pedidos - paso 3
    template_name = 'agregar_pedido_paso_tres.html'

    def get(self, request, *args, **kwargs):
        last_pedido = Pedidos.objects.filter(idUsuario=request.user).latest('id')
        context ={
            'title': '3/3 - Completar el pedido',
            'last_pedido': last_pedido,
            'form': FormularioDetalle(),
            'detalle_pedido': Detalles_Pedido.objects.filter(idPedidos=last_pedido).annotate(total=F('cantidad') * F('precio')),
            'total_pedido': Detalles_Pedido.objects.filter(idPedidos=last_pedido).aggregate(total=Sum(F('cantidad') * F('precio')))['total'],
            'mensajes' : request.session.get('mensajes', None),
        }
        request.session.pop('mensajes', None)
        request.session.pop('idEmpresa', None)
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
            request.session['mensajes'] = {'enviado': True, 'resultado': f'Se ha agregado {producto} al pedido exitosamente'}
            return redirect('nuevo_pedido_paso_tres')
        else:
            mensajes = {'enviado': False, 'resultado': form.errors}

        context = {
            'form': form
        }
        return render(request, self.template_name, context)

class CierrePedidoView(TemplateView):                                                       # Agrega pedidos - cierre del pedido
    template_name = 'cierre_pedido.html'

    def get(self, request, *args, **kwargs):
        request.session.pop('mensajes', None)
        request.session.pop('idEmpresa', None)

        context = {
            'title': '🎉 El pedido está finalizado',
        }

        return render(request, self.template_name, context)