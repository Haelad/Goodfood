from django.contrib import admin
from django.core.paginator import Paginator
from .models import Categories, Goods


# pip install django-infinite-pagination
# Register your models here.

STATUS_CHOICES = {
    "d": "Draft",
    "p": "Published",
    "w": "Withdrawn",
}

@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
  #fields content'
  empty_value_display = "-пусто-"
  readonly_fields = ['time_created', 'time_updated',]

  fieldsets = (
        ('', {
            'classes': ['wide'],
            'fields': ('name','desc', 'category'),
            'description': '[Обязательно] Укажите все поля, пользуйтесь кириллицей или латиницей'
        }),
        ('Фото', {
 
            'fields': ('photo',),
            'description': '[Обязательно] Укажите поле фото размером 100 x 100'
        }),
        ('Информация для администратора', {
            'classes': ['collapse'],
            'fields': ('slugify_name', ('time_created', 'time_updated',) )
        })
    )
  
  # search content
  search_fields = ("name",)
  list_filter = ("category__cat", )

  warn_unsaved_form = True
  list_filter_sheet = True

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
  warn_unsaved_form = True

  search_fields = ("cat",)
  list_filter = ("cat", )



