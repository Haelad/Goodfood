from django.contrib.postgres.search import SearchVector, SearchQuery
from django.db.models.query import QuerySet
from django.db.models import Q

from .models import Goods

class PostgresSearchMixin:
    search_param = "q"
    search_fields = ("name", "desc")  # поля, по которым ищем
    search_language = "russian"       # язык поиска

    def get_search_query(self):
        return self.request.GET.get(self.search_param)

    def get_queryset(self):
        qs = Goods.objects.select_related("category").all()  # ожидаем QuerySet
        query = self.get_search_query()
        if not query:
            return qs

        if isinstance(qs, QuerySet):
            # Создаем SearchVector для нужных полей
            vector = None
            for field in self.search_fields:
                if vector is None:
                    vector = SearchVector(field, config=self.search_language)
                else:
                    vector += SearchVector(field, config=self.search_language)

            search_query = SearchQuery(query, config=self.search_language)

            return qs.annotate(search=vector).filter(search=search_query)

        # fallback для list, если вдруг super() вернул list
        lowered = query.lower()
        def matches(obj):
            for field in self.search_fields:
                val = getattr(obj, field, "")
                if val and lowered in str(val).lower():
                    return True
            return False

        return [obj for obj in qs if matches(obj)]
      
      


class SearchMixin:
    search_param = "q"

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get(self.search_param)
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | Q(desc__icontains=query)
            )
        return queryset