# recetas/urls.py
from django.urls import path
from . import views
from .views import Home

urlpatterns = [
    path('', views.index, name='index'),
    path('recetas', views.recetas, name='recetas'),
    path('boot', views.boot, name='boot'),
    path('home', Home.as_view(), name='home'),
    path('tabla', views.tabla, name='tabla'),
    path('receta_new', views.receta_new, name='receta_new'),
    path('receta_edit/<int:pk>', views.receta_edit, name='receta_edit'),
    path('receta_delete/<int:pk>', views.receta_delete, name='receta_delete'),
]
