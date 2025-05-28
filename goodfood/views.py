from django.shortcuts import redirect, render, get_object_or_404, get_list_or_404
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
  detail_food = get_object_or_404(Goods.objects.select_related("category"), pk=pk, slugify_name=slug_name)
  return render(request, "food.html", {"f" : detail_food})


@cache_page(60*4, key_prefix="goodfood:food_category")
def food_category(request, cat_id):
  food = get_list_or_404(Goods.objects.filter(category_id=cat_id))
  return render(request, "category.html", {"food":food})


# views_handlers
def page_not_found(request, exception):
    return render(request, "handlers/page_404.html", status=404, context={"e": exception}) 

def error_R(request):
    return render(request, "handlers/page_500.html", status=500)




  
  
  

  
