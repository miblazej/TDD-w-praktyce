from typing import Text
from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.
class List(models.Model):
  pass

class Item(models.Model):
  text = models.TextField(default='')
  list = models.ForeignKey(List, default=None, on_delete=models.CASCADE)

  def __str__(self):
    return self.text


