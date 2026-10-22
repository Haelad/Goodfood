from datetime import timedelta
from urllib.parse import urlencode

from django.contrib import admin
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from django.utils.text import Truncator
from django.utils.timesince import timesince
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import (
    RangeDateFilter,
    RangeNumericFilter,
    RelatedDropdownFilter,
)
from unfold.decorators import action, display
from unfold.utils import display_for_label

from .filters import CalorieLevelFilter, PeriodFilter
from .forms import GoodsAdminForm
from .models import DEFAULT_CATEGORY_NAME, Categories, FoodEntry, Goods

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
        "get_kcal_label",
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
            "Пищевая ценность",
            {
                "classes": ["tab"],
                "fields": ("kcal", ("proteins", "fats", "carbs"), "portion_grams"),
                "description": (
                    "На 100 г — как на упаковке. Можно оставить пустым и "
                    "заполнить позже"
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
    actions_detail = ["log_eaten"]
    actions_row = ["log_eaten"]

    class Media:
        js = ("js/admin-photo-preview.js",)

    def get_list_filter(self, request):
        filters = [
            ("category", RelatedDropdownFilter),
            CalorieLevelFilter,
            ("kcal", RangeNumericFilter),
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

    @display(description="Калории", ordering="kcal", label=True)
    def get_kcal_label(self, obj):
        return f"{obj.kcal:g} ккал" if obj.kcal is not None else None

    @action(description="Записать, что съел", url_path="log-eaten", icon="restaurant")
    def log_eaten(self, request, object_id):
        goods = self.get_object(request, object_id)
        params = urlencode({"goods": goods.pk, "grams": goods.portion_grams})
        return redirect(f"{reverse('admin:goodfood_foodentry_add')}?{params}")

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


@admin.register(FoodEntry)
class FoodEntryAdmin(OwnedAdminMixin, ModelAdmin):
    list_display = (
        "get_header",
        "get_grams",
        "get_kcal_label",
        "get_macros",
        "eaten_at",
    )
    list_display_links = ("get_header",)
    list_select_related = ("goods", "goods__category")
    list_filter = (PeriodFilter, ("goods__category", RelatedDropdownFilter))
    list_filter_submit = True
    list_filter_sheet = True
    search_fields = ("goods__name",)
    date_hierarchy = "eaten_at"
    autocomplete_fields = ("goods",)
    fields = ("goods", ("grams", "eaten_at"))
    compressed_fields = True
    # итоги по калориям и БЖУ за отфильтрованный период — над таблицей
    list_before_template = "admin/goodfood/foodentry/totals.html"

    @display(description="Что съели", header=True, ordering="goods__name")
    def get_header(self, obj):
        goods = obj.goods
        image = {"path": goods.photo.url, "squared": True} if goods.photo else None
        return [goods.name, goods.category.cat, goods.name[:1], image]

    @display(description="Вес", ordering="grams")
    def get_grams(self, obj):
        return f"{obj.grams} г"

    @display(description="Калории", label=True)
    def get_kcal_label(self, obj):
        return f"{obj.kcal} ккал" if obj.kcal is not None else None

    @display(description="Б / Ж / У, г")
    def get_macros(self, obj):
        values = [obj.nutrient(name) for name in ("proteins", "fats", "carbs")]
        if all(value is None for value in values):
            return None
        return " / ".join("—" if v is None else str(v) for v in values)

    # ?goods=…&grams=… от кнопки «Записать, что съел» у товара Django сам
    # подставляет в форму добавления как начальные значения

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "goods" and not request.user.is_superuser:
            kwargs["queryset"] = Goods.objects.filter(owner=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
