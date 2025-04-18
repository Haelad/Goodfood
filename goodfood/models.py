from django.db import models
from django.urls import reverse

from django.core.validators import  MaxLengthValidator
from goodfood.validators import GoodfoodValidator

from slugify import slugify



# Create your models here.
class Categories(models.Model):
  
  cat = models.CharField(verbose_name="категория", max_length=256, db_index=True)
    
  class Meta:
      verbose_name = ("Категория")
      verbose_name_plural = ("Категории")
      
  def __str__(self): 
    return self.cat    
      
      
  def get_absolute_url(self):
     return reverse("goodfood:_category", kwargs={"cat_id": self.pk})


class Goods(models.Model):
  
  name = models.CharField(
    verbose_name="Название", max_length=64, db_index=True, editable=True, validators=[MaxLengthValidator(64), GoodfoodValidator()]
    )
  
  photo = models.ImageField(
    verbose_name="Фото", name="photo",
    blank=False, null=False, editable=True,
    )
  
  description = models.TextField(
    verbose_name="Описание", name="desc", max_length=256, unique=False, blank=True, null=True, editable=True, validators=[MaxLengthValidator(256), GoodfoodValidator()]
  )
  
  category = models.ForeignKey(to=Categories, verbose_name="категория", name="category", on_delete=models.PROTECT, validators=[MaxLengthValidator(256), GoodfoodValidator()])
  
  
  slugify_name = models.SlugField(verbose_name="Слаг", blank=True, max_length=256,)
   
  
  class Meta:
      verbose_name = ("Товар")
      verbose_name_plural = ("Товары")

  def __str__(self):
      return self.name
  
  def save(self, *args, **kwargs):
    if not self.slugify_name:
      self.slugify_name = slugify(self.name)
    super(Goods, self).save(*args, **kwargs)
    

  def get_absolute_url(self):
     return reverse("goodfood:_detail", kwargs={"slug_name": self.slugify_name, "pk": self.pk})
      




