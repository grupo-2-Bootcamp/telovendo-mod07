import os
import random
import string
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from django.urls import reverse
from telovendo.form import FormularioLogin, FormularioRegistro, FormularioUpdateEstado
from telovendo.models import Pedidos, CustomUser, Empresas, Direcciones, Detalles_Pedido, Estado_Pedido, Productos

from django.core.mail import send_mail

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
        
        pedido = Pedidos.objects.get(id=idpedido)
        empresa = Empresas.objects.get(id=pedido.idEmpresa_id)
        usuario = CustomUser.objects.get(id=pedido.idUsuario_id)
        direccion = Direcciones.objects.get(id=pedido.idDireccion_id)
        detalle_pedido = Detalles_Pedido.objects.filter(idPedidos=idpedido)
        # productos = []
        # for detalle in detalle_pedido:
        #     productos.append(Productos.objects.get(id=detalle.idProductos_id))
        context ={
            'title': f'Detalle de orden {pedido}',
            'pedido': pedido,
            'empresa': empresa,
            'direccion': direccion,
            'detalle_pedido': detalle_pedido,
            'usuario': usuario,
            # 'productos': productos
            }
        return render(request, self.template_name, context)

class UpdateEstadoPedidoView(TemplateView):
    template_name = 'modifica_estado.html'
        
    def get_context_data(self, idpedido, **kwargs):
        context = super().get_context_data(**kwargs)
        instance = get_object_or_404(Pedidos, id=self.kwargs['idpedido'])
        volver_atras = reverse('detalle_pedido', kwargs={'idpedido': idpedido})
        context= {
            'form' : FormularioUpdateEstado(instance=instance),
            'title': f'Modificar el estado del pedido {idpedido}',
            'pedido': Pedidos.objects.get(id=idpedido),
            'volver_atras': volver_atras,
            }
        return context

    def post(self, request, idpedido, *args, **kwargs):
        instance = get_object_or_404(Pedidos, id=self.kwargs['idpedido'])
        form = FormularioUpdateEstado(request.POST, instance=instance)
        reenvio = reverse('detalle_pedido', kwargs={'idpedido': idpedido})
        if form.is_valid():
            form.save()
            return redirect(reenvio)
        return self.render_to_response(self.get_context_data())


class RegistroView(TemplateView):           # Vista de registro de usuarios 
    template_name = 'registro.html'

    
    def get(self, request, *args, **kwargs):
        form = FormularioRegistro()
        title = 'Registro de Usuario'
        context = {
            'formulario': form, 
            'title': title
            }
        
        return render(request, self.template_name, context )

    def post(self, request, *args, **kwargs):
        form = FormularioRegistro(request.POST, request.FILES)
        title = 'Registro de Usuarios'
        if form.is_valid():
            username = form.cleaned_data['username']
            password = generate_random_password()
            user = form.save(commit = False)
            # group = form.cleaned_data['group']
            # if group:
            #     group.user_set.add(user)
            user.set_password(password)
            user.save()
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

        return render(request, self.template_name, context)

