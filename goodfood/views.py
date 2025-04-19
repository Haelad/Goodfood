from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views.decorators.cache import cache_page

from .models import Goods, Categories




# Create your views here.


def index(request):

  return render(request, "index.html")


@cache_page(60*4, key_prefix="goodfood:food_list")
def food(request):
  food = Goods.objects.all()
  food_category = Categories.objects.all()
  
  context = list(food) + list(food_category)
  # food = get_list_or_404(Goods.objects.select_related("category").filter(is_active=True))
  # food = get_list_or_404(Goods, select_related="category", is_active=True)
  return render(request, "goods.html", {"context" : context})


@cache_page(60, key_prefix="goodfood:food_detail")
def food_detail(request, slug_name, pk):
  detail_food = get_object_or_404(Goods, pk=pk)
  return render(request, "food.html", {"f" : detail_food})


@cache_page(60*4, key_prefix="goodfood:food_category")
def food_category(request, cat_id):
  food = Goods.objects.filter(category_id=cat_id)
  food_category = Categories.objects.all()

  # food = get_list_or_404(Goods.objects.filter(category_id=cat_id))
  # food = get_list_or_404(Goods, select_related="category", category_id=cat_id)  
  return render(request, "category.html", {"food":food, "cat":food_category})
  
  
  

  
