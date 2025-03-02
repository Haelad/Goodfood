from django.shortcuts import render

from .models import Goods, Categories




# Create your views here.


def index(request):

  return render(request, "index.html")


def goods(request):
  
  goods = Goods.objects.all()
  

  

  
    
  
  
  return render(request, "goods.html", {"goods" : goods})
  
  
