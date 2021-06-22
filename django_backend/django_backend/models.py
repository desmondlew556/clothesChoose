from django.db import models
from django import forms
import os
from django.conf import settings

#add on library for colors
#from colorfield.fields import ColorField

#number values for char length 
short_len=100
middle_len=500
long_len = 1000

    
class Characteristics(models.Model):
    characteristic_name = models.CharField(primary_key = True, max_length = short_len)

#class Color(models.Model):
    #colors = ColorField(default=None)

class Garment(models.Model):
    #ranking_initializer = lambda x: {'rank_'+str(rank+1):0 for rank in range(10)}
    #def ranking_initializer():
    #    return {'rank_'+str(rank+1):0 for rank in range(10)}
    image_path=models.CharField(max_length = middle_len)
    #colors = models.ManyToManyField(Color)
    characteristics = models.ManyToManyField(Characteristics)
    count_for_each_ranking=models.JSONField(default = {'rank_'+str(rank+1):0 for rank in range(10)})
    def __str__(self):
        return self.image_path
    class Meta:
        abstract = True

class GarmentMen(Garment):
    def __str__(self):
        return self.image_path

class GarmentWomen(Garment):
    def __str__(self):
        return self.image_path

class GarmentOthers(Garment):
    garment_type_options = [
        ("U","Unisex"),
        (None,"Unknown")
    ]
    garment_type = models.CharField(
        choices = garment_type_options,
        max_length = short_len
    )

