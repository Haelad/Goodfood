from datetime import timedelta

from django.contrib import admin
from django.db.models import Count
from django.utils import timezone
from django.utils.html import format_html
from django.utils.text import Truncator
from django.utils.timesince import timesince
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import RangeDateFilter, RelatedDropdownFilter
from unfold.decorators import display
from unfold.utils import display_for_label

from .forms import GoodsAdminForm
from .models import DEFAULT_CATEGORY_NAME, Categories, Goods

NEW_PERIOD = timedelta(days=3)
FRESHNESS_LABELS = {"new": "success", "old": "info"}
COUNT_LABELS = {"has": "success", "empty": "default"}


class OwnedAdminMixin:
    """Суперпользователь видит всё, остальные — только свои объекты."""

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.owner = request.user
        super().save_model(request, obj, form, change)


@admin.register(Goods)
class GoodsAdmin(OwnedAdminMixin, ModelAdmin):
    form = GoodsAdminForm
    list_display = (
        "get_header",
        "get_category_label",
        "get_freshness_label",
        "owner",
        "time_updated",
    )
    list_display_links = ("get_header",)
    list_select_related = ("category", "owner")
    list_per_page = 25
    empty_value_display = "—"
    readonly_fields = [
        "time_created",
        "time_updated",
        "get_status_label",
        "slugify_name",
    ]
    fieldsets = (
        (
            "Основное",
            {
                "classes": ["tab"],
                "fields": ("name", "desc", ("category", "new_category")),
                "description": (
                    "Пользуйтесь кириллицей или латиницей. Категорию можно "
                    "выбрать, вписать новую или оставить пустой"
                ),
            },
        ),
        (
            "Фото",
            {
                "classes": ["tab"],
                "fields": ("photo",),
                "description": (
                    "Рекомендуемый размер фото — 100 × 100. "
                    "Превью обновляется сразу после выбора файла"
                ),
            },
        ),
        (
            "Служебное",
            {
                "classes": ["tab"],
                "fields": (
                    "get_status_label",
                    "slugify_name",
                    ("time_created", "time_updated"),
                ),
            },
        ),
    )
    search_fields = ("name", "desc")
    autocomplete_fields = ("category",)
    date_hierarchy = "time_created"
    warn_unsaved_form = True
    compressed_fields = True
    list_filter_submit = True
    list_filter_sheet = True

    class Media:
        js = ("js/admin-photo-preview.js",)

    def get_list_filter(self, request):
        filters = [
            ("category", RelatedDropdownFilter),
            ("time_created", RangeDateFilter),
        ]
        if request.user.is_superuser:
            filters.append(("owner", RelatedDropdownFilter))
        return filters

    @display(description="Товар", header=True, ordering="name")
    def get_header(self, obj):
        image = {"path": obj.photo.url, "squared": True} if obj.photo else None
        return [
            obj.name,
            Truncator(obj.desc or "").chars(60),
            obj.name[:1],
            image,
        ]

    @display(description="Категория", label=True, ordering="category__cat")
    def get_category_label(self, obj):
        return obj.category.cat

    @display(description="Статус", label=FRESHNESS_LABELS)
    def get_freshness_label(self, obj):
        if obj.time_created >= timezone.now() - NEW_PERIOD:
            return "new", "Новинка"
        return "old", "В каталоге"

    @display(description="Статус товара")
    def get_status_label(self, obj):
        # label= для readonly-полей формы не применяется, рендерим вручную
        if not obj.pk:
            return "Сохраните товар, чтобы увидеть статус"
        label = display_for_label(
            self.get_freshness_label(obj), self.empty_value_display, FRESHNESS_LABELS
        )
        return format_html(
            '{} <span class="ml-2 text-xs">обновлено {} назад</span>',
            label,
            timesince(obj.time_updated),
        )

    def get_changeform_initial_data(self, request):
        initial = super().get_changeform_initial_data(request)
        default = Categories.objects.filter(
            owner=request.user, cat=DEFAULT_CATEGORY_NAME
        ).first()
        if default:
            initial.setdefault("category", default.pk)
        return initial

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.owner = request.user
        # Новая категория принадлежит владельцу рецепта, а не тому, кто редактирует
        obj.category = form.resolve_category(obj.owner)
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category" and not request.user.is_superuser:
            kwargs["queryset"] = Categories.objects.filter(owner=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Categories)
class CategoriesAdmin(OwnedAdminMixin, ModelAdmin):
    list_display = ("cat", "get_goods_count_label", "owner")
    fields = ("cat", "get_goods_count_field")
    readonly_fields = ["get_goods_count_field"]
    search_fields = ("cat",)
    warn_unsaved_form = True
    compressed_fields = True
    list_filter_sheet = True

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(goods_count=Count("goods"))

    @display(description="Товаров", ordering="goods_count", label=COUNT_LABELS)
    def get_goods_count_label(self, obj):
        count = getattr(obj, "goods_count", None)
        if count is None:
            count = obj.goods_set.count()
        return ("has" if count else "empty"), str(count)

    @display(description="Товаров в категории")
    def get_goods_count_field(self, obj):
        if not obj.pk:
            return "Сохраните категорию, чтобы увидеть количество товаров"
        return display_for_label(
            self.get_goods_count_label(obj), self.empty_value_display, COUNT_LABELS
        )
