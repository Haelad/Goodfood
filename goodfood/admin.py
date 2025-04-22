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
  # paginator = Paginator
  # show_full_result_count = False

  #fields content
  readonly_fields = ['time_created', 'time_updated', 'slugify_name']
  # fields = ['name', 'desc', 'photo', 'category', 'slugify_name', ('time_created', 'time_updated')]
  fieldsets = (
        ('', {
            'fields': ('name','desc', 'category')
        }),
        ('Фото', {
            'fields': ('photo',)  
        }),
        ('Дата для администратора', {
            'fields': (('time_created', 'time_updated'), 'slugify_name' )
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



