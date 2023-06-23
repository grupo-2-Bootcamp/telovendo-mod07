from django.shortcuts import render, redirect
from django.views.generic import TemplateView

# Create your views here.

class Index(TemplateView):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        title = "Bienvenido a TeLoVendo"
        return render(request, self.template_name, {"title": title})