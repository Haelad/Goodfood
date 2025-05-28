from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.decorators.cache import cache_page

from .models import Goods, Categories

# сделать 404

def index(request):
  return render(request, "index.html")

# Настроить более точное кеширование отдельно темплейты и view
@cache_page(60*4, key_prefix="goodfood:food_list")
def food(request):
  list_food = get_list_or_404(Goods.objects.select_related("category").all())
  

  return render(request, "goods.html", {"context" : list_food})


@cache_page(60, key_prefix="goodfood:food_detail")
def food_detail(request, slug_name, pk):
  detail_food = get_object_or_404(Goods, pk=pk)
  return render(request, "food.html", {"f" : detail_food})


@cache_page(60*4, key_prefix="goodfood:food_category")
def food_category(request, cat_id):
  food = get_list_or_404(Goods.objects.filter(category_id=cat_id))

  return render(request, "category.html", {"food":food})
  
  
  

  
