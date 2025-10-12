from slugify import slugify

from django.db import models
from django.urls import reverse
from django.core.validators import  MinLengthValidator, MaxLengthValidator, RegexValidator

from apps.goodfood.validators import GoodfoodValidator





# Create your models here.
class Categories(models.Model):
  
  cat = models.CharField(verbose_name='категория', max_length=32, db_index=True, validators=[MinLengthValidator(1), MaxLengthValidator(32), GoodfoodValidator()])
    
  class Meta:
      verbose_name = ('Категория')
      verbose_name_plural = ('Категории')
      
  def __str__(self): 
    return self.cat    
      
      
  def get_absolute_url(self):
     return reverse('goodfood:_category', kwargs={'cat_id': self.pk})


class Goods(models.Model):
  
  name = models.CharField(
    verbose_name='Название', max_length=64, db_index=True, editable=True, validators=[MinLengthValidator(1), MaxLengthValidator(64),  GoodfoodValidator()]
    )
  
  photo = models.ImageField(
    verbose_name='Фото', name='photo',
    blank=False, null=False, editable=True,
    )
  
  description = models.TextField(
    verbose_name='Описание', name='desc', max_length=256, unique=False, blank=True, null=True, editable=True, validators=[MinLengthValidator(1), MaxLengthValidator(256), GoodfoodValidator()]
  )
  
  category = models.ForeignKey(to=Categories, verbose_name='категория', name='category', on_delete=models.PROTECT)
  
  
  slugify_name = models.SlugField(max_length=256, blank=True, unique=True, allow_unicode=True, verbose_name="Слаг", validators=[
            RegexValidator(
                regex=r'^[-a-zA-Z0-9_]+$',
                message='Slug может содержать только буквы, цифры, дефис и подчёркивания.'
            )
        ])
  
  time_created = models.DateTimeField(verbose_name='Время создания', auto_now_add=True, editable=False )
  time_updated = models.DateTimeField(verbose_name='Время изменения', auto_now=True, editable=True)
   
  
  class Meta:
      verbose_name = ('Товар')
      verbose_name_plural = ('Товары')

      db_table_comment = 'База данных с рецептами блюд'

      ordering = ['-time_created']

      #The name of a field or a list of field names in the model, typically DateField, DateTimeField, or IntegerField. 
      #This specifies the default field(s) to use in your model Manager’s latest() and earliest() methods.
      get_latest_by = ['time_updated']

      # разрешения для тех кто может добавлять, редактировать, изменять - https://docs.djangoproject.com/en/5.2/ref/models/options/#permissions
      # permissions = [()]

  def __str__(self):
      return self.name
  
  def save(self, *args, **kwargs):
    if not self.slugify_name:
      self.slugify_name = slugify(self.name)
    super(Goods, self).save(*args, **kwargs)
    

  def get_absolute_url(self):
     return reverse("goodfood:_detail", kwargs={"slug_name": self.slugify_name, "pk": self.pk})
      




