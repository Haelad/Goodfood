from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify

# Create your models here.





class Categories(models.Model):
  
  cat = models.CharField(verbose_name="Категория", name="category", max_length=64, db_index=True)
  
  class Meta:
      verbose_name = _("Категория")
      verbose_name_plural = _("Категории")

  def __str__(self):
      return self.name

  def get_absolute_url(self):
      return reverse("_detail", kwargs={"pk": self.pk})


class Goods(models.Model):
  
  name = models.CharField(
    verbose_name="Название", name="product_name", max_length=64, db_index=True, editable=True,
    )
  
  photo = models.ImageField(
    verbose_name="Фото", name="photo", 
    width_field=..., height_field=..., upload_to=...,storage=..., 
    blank=False, null=False, editable=True
    )
  
  description = models.TextField(
    verbose_name="Описание", name="desc", max_length=256, unique=False, blank=True, null=True, editable=True,
  )
  
  category = models.ForeignKey(to=Categories, verbose_name="Категория", name="category", on_delete=...,)
  
  
  slugify_name = models.SlugField(verbose_name="Слаг", name="slug", max_length="256", blank=..., null=..., editable=...)
   
  
  class Meta:
      verbose_name = _("Товар")
      verbose_name_plural = _("Товары")

  def __str__(self):
      return self.name
  
  def save(self, *args, **kwargs):
    if not self.id:
      self.slugify_name = slugify(self.name)
    super(Goods, self).save(*args, **kwargs)
    

  def get_absolute_url(self):
      return reverse("_detail", kwargs={"pk": self.pk})
      




