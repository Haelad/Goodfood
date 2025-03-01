from django.contrib import admin
from .models import Categories, Goods

# Register your models here.


class GoodsAdmin(admin.ModelAdmin):
  pass


class CategoriesAdmin(admin.ModelAdmin):
  pass


admin.site.register(Goods, GoodsAdmin)
admin.site.register(Categories, CategoriesAdmin)
