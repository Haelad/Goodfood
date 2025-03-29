from django.shortcuts import render

from .models import Goods, Categories




# Create your views here.


def index(request):

  return render(request, "index.html")


def food(request):
  
  food = Goods.objects.all()

  food_category = Categories.objects.all()
  
  
  return render(request, "goods.html", {"goods" : food, "cat": food_category})



def food_detail(request, slug_name, pk):
  
  detail_food = Goods.objects.get(pk=pk)

  return render(request, "food.html", {"f" : detail_food})


def food_category(request, cat_id):
  
  
  food = Goods.objects.filter(category_id=cat_id)
  
  food_category = Categories.objects.all()
  
  return render(request, "category.html", {"food":food, "cat":food_category})
  
  
  
