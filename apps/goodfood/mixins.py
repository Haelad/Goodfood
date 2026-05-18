from django.contrib.postgres.search import SearchQuery, SearchVector, TrigramSimilarity
from django.db.models import Q
from django.db.models.query import QuerySet


class PostgresSearchMixin:
    search_param = "q"
    search_fields = ("name", "desc")
    search_language = "russian"

    def get_search_query(self):
        return self.request.GET.get(self.search_param)

    def get_queryset(self):
        qs = super().get_queryset().select_related("category")
        query = self.get_search_query()
        if not query:
            return qs
        if isinstance(qs, QuerySet):
            vector = None
            for field in self.search_fields:
                if vector is None:
                    vector = SearchVector(field, config=self.search_language)
                else:
                    vector += SearchVector(field, config=self.search_language)

            search_query = SearchQuery(query, config=self.search_language)
            return qs.annotate(
                search=vector,
                similarity=TrigramSimilarity("name", query),
            ).filter(Q(search=search_query) | Q(similarity__gt=0.2))


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
