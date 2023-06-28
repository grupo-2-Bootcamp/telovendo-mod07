from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView

from telovendo.form import FormularioLogin, FormularioRegistro
from telovendo.models import Pedidos, CustomUser

from django.contrib.auth.models import Group
from django.views import View

# Create your views here.

class LoginView(TemplateView):
    template_name = "login.html"
    def get(self, request, *args, **kwargs):
        formulario = FormularioLogin()
        title = "Acceso al sitio interno"
        return render(request, self.template_name, {"formulario": formulario, "title": title,})
    
    def post(self, request, *args, **kwargs):
        title = "Acceso al sitio interno"
        form = FormularioLogin(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('internal')
                    # if request.user.groups.filter(name='Trabajadores').exists():
                    #     return redirect('sitiointerno-trabajadores')
                    # elif request.user.groups.filter(name='Clientes').exists():
                    #     return redirect('sitiointerno-clientes')
                    # elif request.user.groups.filter(name='Proveedores').exists():
                    #     return redirect('sitiointerno-proveedores')
                    # else:
                        # return redirect('index')
            form.add_error("username", "Se han ingresado las credenciales equivocados.")
            return render(request, self.template_name, { "form": form, "title": title,})
        else:
            return render(request, self.template_name, { "form": form, "title": title,})
        
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
            user = form.save()
            group = form.cleaned_data['group']
            if group:
                group.user_set.add(user)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            user.save()
            mensajes = {"enviado": True, "resultado": "Has creado un nuevo usuario exitosamente"}
        else:
            mensajes = {"enviado": False, "resultado": form.errors}
        context = {
            "formulario": form,
            "mensajes": mensajes,
            "titulo": titulo
        }
        return render(request, self.template_name, context)

# class RegistroView(View):
#     template_name = 'registro.html'

#     class Meta:
#         model = CustomUser
#         fields = ('username', 'password1', 'password2',)

#     def get(self, request, *args, **kwargs):
#         form = FormularioRegistro()
#         titulo = "Registro de Usuario"
#         context = {
#             "formulario": form,
#             "titulo": titulo
#         }
#         return render(request, self.template_name, context)

#     def post(self, request, *args, **kwargs):
#         form = FormularioRegistro(request.POST, request.FILES)
#         titulo = "Registro de Usuarios"
#         if form.is_valid():
#             user = form.save(commit=False)
#             group = form.cleaned_data['group']
#             if group:
#                 group.user_set.add(user)
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password1']
#             user.set_password(password)
#             user.save()
#             mensajes = {"enviado": True, "resultado": "Has creado un nuevo usuario exitosamente"}
#         else:
#             mensajes = {"enviado": False, "resultado": form.errors}
#         context = {
#             "formulario": form,
#             "mensajes": mensajes,
#             "titulo": titulo
#         }
#         return render(request, self.template_name, context)
    
