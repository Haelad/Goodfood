import logging

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.db import DatabaseError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView, TemplateView

from .mixins import PostgresSearchMixin, TodayDiaryMixin
from .models import FoodEntry, Goods

logger = logging.getLogger(__name__)

# TODO: вынести общее кэширование queryset и формат ключей


class IndexView(TemplateView):
    template_name = "goodfood/index.html"


class FoodListView(LoginRequiredMixin, TodayDiaryMixin, PostgresSearchMixin, ListView):
    model = Goods
    template_name = "goodfood/goods.html"
    context_object_name = "context"
    paginate_by = 12

    def get_queryset(self):
        cache_key = f"goods:food:user:{self.request.user.pk}"
        goods = cache.get(cache_key)

        if goods is None:
            try:
                goods = list(super().get_queryset().filter(owner=self.request.user))
            except DatabaseError:
                logger.exception("could not find module in queryset")
                raise

            try:
                cache.set(cache_key, goods, 300)
            except Exception:
                logger.exception("Could not save goods to cache")
                return super().get_queryset().filter(owner=self.request.user)

        return goods


class FoodDetailView(LoginRequiredMixin, DetailView):
    model = Goods
    template_name = "goodfood/food.html"
    context_object_name = "food"

    slug_field = "slugify_name"
    slug_url_kwarg = "slug_name"
    pk_url_kwarg = "pk"

    def get_queryset(self):
        cache_key = (
            f"goods:detail-food:user:{self.request.user.pk}:pk:{self.kwargs['pk']}"
        )
        goods = cache.get(cache_key)

        if goods is None:
            try:
                goods = super().get_queryset().filter(owner=self.request.user)
            except DatabaseError:
                logger.exception("could not find module in queryset")
                raise

            try:
                cache.set(cache_key, goods, 300)
            except Exception:
                logger.exception("Could not save detail-food to cache")
                return super().get_queryset().filter(owner=self.request.user)

        return goods


class FoodCategoryView(LoginRequiredMixin, TodayDiaryMixin, ListView):
    model = Goods
    template_name = "goodfood/category.html"
    context_object_name = "food"

    def get_queryset(self):
        cache_key = (
            f"goods:category-food:user:{self.request.user.pk}:"
            f"cat_id:{self.kwargs['cat_id']}"
        )

        goods = cache.get(cache_key)

        if goods is None:
            try:
                goods = list(
                    super()
                    .get_queryset()
                    .filter(owner=self.request.user, category_id=self.kwargs["cat_id"])
                )
            except DatabaseError:
                logger.exception("could not find module in queryset")
                raise

            try:
                cache.set(cache_key, goods, 300)
            except Exception:
                logger.exception("Could not save category-food to cache")
                return super().get_queryset().filter(owner=self.request.user)

        return goods


# Быстрый дневник: «+» и «−» на карточках блюд


def _today_state(request, goods):
    today = FoodEntry.objects.filter(owner=request.user).today()
    totals = today.totals()
    return JsonResponse(
        {
            "count": today.filter(goods=goods).count(),
            "totals": {name: str(value) for name, value in totals.items()},
        }
    )


@login_required
@require_POST
def eat(request, pk):
    """Записать обычную порцию блюда на текущее время."""
    goods = get_object_or_404(Goods, pk=pk, owner=request.user)
    FoodEntry.objects.create(owner=request.user, goods=goods, grams=goods.portion_grams)
    return _today_state(request, goods)


@login_required
@require_POST
def uneat(request, pk):
    """Отменить последнюю сегодняшнюю запись этого блюда."""
    goods = get_object_or_404(Goods, pk=pk, owner=request.user)
    last = (
        FoodEntry.objects.filter(owner=request.user, goods=goods)
        .today()
        .order_by("-eaten_at", "-pk")
        .first()
    )
    if last:
        last.delete()
    return _today_state(request, goods)


# views_handlers
def page_not_found(request, exception):
    return render(
        request, "handlers/page_404.html", status=404, context={"e": exception}
    )


def error_R(request):
    return render(request, "handlers/page_500.html", status=500)
