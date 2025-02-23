from django.urls import path
from .views import index_view

app_name = "goodfood"

urlpatterns = [path("", index_view, name="main")]