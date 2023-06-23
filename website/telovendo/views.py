from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from telovendo.form import FormularioLogin

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
                    return redirect('interno')
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
        title = "Bienvenidos al Sitio Interno de Telovendo"
        return render(request, self.template_name, {"title": title,})