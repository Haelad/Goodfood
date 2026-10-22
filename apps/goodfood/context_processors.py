from django.db.models import Count

from .models import Categories


def nav_categories(request):
    """Категории пользователя для фильтра в шапке (только непустые)."""
    if not request.user.is_authenticated:
        return {}
    categories = (
        Categories.objects.filter(owner=request.user)
        .annotate(goods_count=Count("goods"))
        .filter(goods_count__gt=0)
        .order_by("cat")
    )
    return {"nav_categories": categories}
