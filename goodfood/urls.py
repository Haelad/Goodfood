from django.urls import path
from goodfood import views
 
app_name = "goodfood"

urlpatterns = [path("", views.index, name="main"),
               path()
               ]