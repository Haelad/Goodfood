from django.urls import path
from apps.goodfood import views
 
app_name = "goodfood"


urlpatterns = [path("", views.index, name="main"),
               path("food/", views.food, name="goods"),
               path("food/<slug:slug_name>/<int:pk>", views.food_detail, name="_detail"),
               path("food/<int:cat_id>", views.food_category, name="_category")
               
               ]

