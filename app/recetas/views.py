# recetas/views.py
from django.shortcuts import  HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.template import loader
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib import messages
from .models import Receta
from .forms import RecetaForm

from django.views.generic import TemplateView


# Create your views here.

def index(request):
    return HttpResponse('Hello World!')

############################  
#Todas las recetas
############################
def recetas(request):
    recetas = Receta.objects.all()
    return render(request, 'recetas.html', {'recetas': recetas})

############################  
#Blanco
############################
def boot(request):
    return render(request, 'boot.html', {})

############################  
#Receta búsqueda
############################
def tabla(request):
    if request.method == 'POST':
        if Receta.objects.filter(nombre = request.POST.get('Buscar')).exists():
            receta = Receta.objects.get(nombre = request.POST.get('Buscar'))
            return render(request, 'tabla.html', {'receta': receta})
        else:
            return render(request, 'error404.html', {'name': request.POST.get('Buscar')})
    else:
        return render(request, 'error.html', {})

############################  
#Añadir una receta
############################
def receta_new(request):
    if request.method == "POST":
        form = RecetaForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            messages.success(request, 'Receta añadida correctamente')
            return redirect('recetas')
        else:
            messages.error(request, 'ERROR. Revise los datos introducidos.')
            return render(request, 'receta_edit.html', {'form': form})
    else:
        form = RecetaForm()
        return render(request, 'receta_edit.html', {'form': form})

############################  
#Editar una receta
############################
def receta_edit(request, pk):
    receta = get_object_or_404(Receta, pk=pk)
    if request.method == "POST":
        form = RecetaForm(request.POST, request.FILES, instance=receta)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            messages.success(request, 'Receta modificada correctamente')
            return redirect('recetas')
        else:
            messages.error(request, 'ERROR. Revise los datos introducidos.')
            return render(request, 'receta_edit.html', {'form': form})
    else:
        form = RecetaForm(instance=receta)
        return render(request, 'receta_edit.html', {'form': form})

    
############################  
#Borrar una receta
############################
def receta_delete(request, pk):
    receta = get_object_or_404(Receta, pk=pk)
    #if request.method == "POST":
     #   if 'delete' in request.POST:
    Receta.objects.filter(pk=pk).delete()
    messages.success(request, 'Receta eliminada correctamente')
    return redirect('recetas')
    #    else:
     #       return render(request, 'error.html', {})
    #else:
    #    return render(request, 'recetas.html', {})

class Home(TemplateView):
    template_name = 'home.html'