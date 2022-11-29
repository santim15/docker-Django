# recetas/models.py
from django.db import models

from django.core.exceptions import ValidationError

def validate_caps(value):
  if value != value.capitalize():
    raise ValidationError('Debe empezar con mayúscula: %(value)s', code='invalid', params={'value': value})

class Receta(models.Model):
  nombre       = models.CharField(max_length=200, validators=[validate_caps])
  preparación  = models.TextField(max_length=5000, validators=[validate_caps])
  foto         = models.ImageField(upload_to='media/fotos') 
  
  def __str__(self):
    return self.nombre
  
class Ingrediente(models.Model):
  nombre        = models.CharField(max_length=100)
  cantidad      = models.PositiveSmallIntegerField()
  unidades      = models.CharField(max_length=5)
  receta        = models.ForeignKey(Receta, on_delete=models.CASCADE)

  def __str__(self):
    return self.nombre