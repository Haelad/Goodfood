from django.urls import path
from apps.goodfood import views
 
app_name = "goodfood"


urlpatterns = [path("", views.IndexView.as_view(), name="main"),
               path("food/", views.FoodListView.as_view(), name="goods"),
               path("food/<slug:slug_name>/<int:pk>", views.FoodDetailView.as_view(), name="_detail"),
               path("food/<int:cat_id>", views.FoodCategoryView.as_view(), name="_category")
               
               ]

