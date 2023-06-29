import os
import random
import string
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from telovendo.form import FormularioLogin, FormularioRegistro
from telovendo.models import Pedidos, CustomUser

from django.core.mail import send_mail

# Create your views here.
def generate_random_password():
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for _ in range(6))
    return password

class LoginView(TemplateView):
    template_name = "login.html"

    def get(self, request, *args, **kwargs):
        formulario = FormularioLogin()
        title = "Acceso al sitio interno"
        return render(request, self.template_name, {"formulario": formulario, "title": title})

    def post(self, request, *args, **kwargs):
        title = "Acceso al sitio interno"
        form = FormularioLogin(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = CustomUser.objects.filter(email=email).first()
            if user is not None:
                if user.is_active:
                    authenticated_user = authenticate(request, username=user.username, password=password)
                    login(request, authenticated_user)
                    return redirect('internal')
            form.add_error("email", "Se han ingresado las credenciales equivocadas.")
        return render(request, self.template_name, {"form": form, "title": title})
        
class InternoView(TemplateView):
    template_name = "internal.html"
    def get(self, request, *args, **kwargs):
        title = "Bienvenido al sistema de compras"
        return render(request, self.template_name, {"title": title,})

class PedidosView(TemplateView):
    template_name = "pedidos.html"

    def get(self, request, *args, **kwargs):
        title = "Bienvenido a la vista de pedidos"
        pedidos = Pedidos.objects.all()

        context ={
            'titulo':title,
            'pedidos': pedidos
        }
        return render(request,self.template_name, context)

class RegistroView(TemplateView):
    template_name = 'registro.html'

    
    def get(self, request, *args, **kwargs):
        form = FormularioRegistro()
        titulo = "Registro de Usuario"
        context = {
            "formulario": form, 
            "titulo": titulo
            }
        
        return render(request, self.template_name, context )

    def post(self, request, *args, **kwargs):
        form = FormularioRegistro(request.POST, request.FILES)
        titulo = "Registro de Usuarios"
        if form.is_valid():
            username = form.cleaned_data['username']
            password = generate_random_password()
            user = form.save(commit = False)
            # group = form.cleaned_data['group']
            # if group:
            #     group.user_set.add(user)
            user.set_password(password)
            user.save()
            mensajes = {"enviado": True, "resultado": "Has creado un nuevo usuario exitosamente"}
        else:
            mensajes = {"enviado": False, "resultado": form.errors}
        correo_destino = form.cleaned_data['email']
        context = {
            "formulario": form,
            "mensajes": mensajes,
            "titulo": titulo
        }

        mensaje = f"""
                Bienvenido a Telovendo.
                Gracias por registrarte en nuestro sitio web. A continuación se le adjunta su contraseña de acceso
                contraseña :   {password} 
                Muchas Gracias por su preferencia
                    """
        send_mail(
            '[TE LO VENDO] - Contraseña',
            mensaje,
            os.environ.get('EMAIL_HOST_USER'),  # Usar el correo configurado en settings.py
            [correo_destino],  # Enviar el correo al destinatario ingresado por el usuario
            fail_silently=False
        )

        return render(request, self.template_name, context)

