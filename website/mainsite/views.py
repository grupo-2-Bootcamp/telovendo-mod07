from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from telovendo.models import Productos, Categoria 

# Create your views here.

class Index(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        title = 'Bienvenido a TeLoVendo'
        return render(request, self.template_name, {'title': title})

class CatalogoIndex(TemplateView):
    template_name = 'catalogo_index.html'

    def get(self, request, *args, **kwargs):
        
        context = {
                'title' : 'Catálogo',
                'categorias': Categoria.objects.all().order_by('nombre'),
        }
        return render(request, self.template_name, context)
    
class CatalogoList(TemplateView):
    template_name = 'catalogo_list.html'

    def get(self, request, *args, **kwargs):
        productos = Productos.objects.filter(categoria=self.kwargs['id_categoria']).order_by('id')
        context = {
                'title' : 'Catálogo',
                'categorias': Categoria.objects.all().order_by('nombre'),
                'categoria': Categoria.objects.get(id=self.kwargs['id_categoria']),
                'productos': productos,
                'cantidad_productos': len(productos),
        }
        return render(request, self.template_name, context)