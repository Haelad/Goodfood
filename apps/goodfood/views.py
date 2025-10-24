from django.shortcuts import redirect, render, get_object_or_404, get_list_or_404
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, TemplateView




from .models import Goods
from .mixins import PostgresSearchMixin, SearchMixin 

# Настроить более точное кеширование отдельно темплейты и view

class IndexView(TemplateView):
    template_name = "goodfood/index.html"


class FoodListView(SearchMixin, ListView):
    model = Goods
    template_name = "goodfood/goods.html"
    context_object_name = "context"
    paginate_by = 12  




@method_decorator(cache_page(300), name='dispatch')
class FoodDetailView(DetailView):
    model = Goods
    template_name = "goodfood/food.html"
    context_object_name = "food"

    slug_field = "slugify_name"
    slug_url_kwarg = "slug_name"
    pk_url_kwarg = "pk"

    def get_object(self):
        pk = self.kwargs.get("pk")
        slug = self.kwargs.get("slug_name")
        return get_object_or_404(Goods, pk=pk, slugify_name=slug)

@method_decorator(cache_page(300), name='dispatch')
class FoodCategoryView(ListView):
    model = Goods
    template_name = "goodfood/category.html"
    context_object_name = "food"

    def get_queryset(self):
        cat_id = self.kwargs.get("cat_id")
        return get_list_or_404(Goods.objects.filter(category_id=cat_id))

# views_handlers
def page_not_found(request, exception):
    return render(request, "handlers/page_404.html", status=404, context={"e": exception}) 

def error_R(request):
    return render(request, "handlers/page_500.html", status=500)




  
  
  

  
