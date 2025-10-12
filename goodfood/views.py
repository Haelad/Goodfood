from django.shortcuts import redirect, render, get_object_or_404, get_list_or_404


from .models import Goods, Categories

# сделать 404

def index(request):
  return render(request, "goodfood/index.html")

# Настроить более точное кеширование отдельно темплейты и view

def food(request):
  list_food = get_list_or_404(Goods.objects.select_related("category").all())
  return render(request, "goodfood/goods.html", context={"context": list_food})


def food_detail(request, slug_name, pk):
  detail_food = get_object_or_404(Goods.objects.select_related("category"), pk=pk, slugify_name=slug_name)
  return render(request, "goodfood/food.html", {"food" : detail_food})



def food_category(request, cat_id):
  cat_food = get_list_or_404(Goods.objects.filter(category_id=cat_id))
  return render(request, "goodfood/category.html", {"food":cat_food})


# views_handlers
def page_not_found(request, exception):
    return render(request, "handlers/page_404.html", status=404, context={"e": exception}) 

def error_R(request):
    return render(request, "handlers/page_500.html", status=500)




  
  
  

  
