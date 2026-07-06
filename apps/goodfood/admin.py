from datetime import timedelta

from django.contrib import admin
from django.utils import timezone
from django.utils.html import format_html
from django.utils.timesince import timesince
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import RangeDateFilter, RelatedDropdownFilter
from unfold.decorators import display

from .models import Categories, Goods


def badge(text, bg, color):
    """Рендерит цветной бэйдж для admin list/detail."""
    style = (
        f"background-color:{bg}; color:{color}; "
        "padding:4px 12px; border-radius:999px; "
        "font-weight:600; font-size:12px;"
    )
    return format_html('<span style="{}">{}</span>', style, text)


@admin.register(Goods)
class GoodsAdmin(ModelAdmin):
    list_display = (
        "get_thumbnail",
        "name",
        "get_category_badge",
        "get_freshness_badge",
        "owner",
        "time_updated",
    )
    empty_value_display = "-пусто-"
    readonly_fields = [
        "time_created",
        "time_updated",
        "get_photo_preview",
        "get_status_badge_field",
        "slugify_name",
    ]
    fieldsets = (
        (
            "",
            {
                "classes": ["wide"],
                "fields": ("name", "desc", "category"),
                "description": (
                    "[Обязательно] Укажите все поля, "
                    "пользуйтесь кириллицей или латиницей"
                ),
            },
        ),
        (
            "Фото",
            {
                "fields": ("photo", "get_photo_preview"),
                "description": ("[Обязательно] Укажите поле фото размером 100 x 100"),
            },
        ),
        (
            "Дополнительная информация",
            {
                "classes": ["collapse"],
                "fields": (
                    "get_status_badge_field",
                    ("time_created", "time_updated"),
                ),
            },
        ),
    )
    search_fields = ("name",)
    warn_unsaved_form = True
    list_filter_sheet = True

    def get_list_filter(self, request):
        if request.user.is_superuser:
            return (
                ("category", RelatedDropdownFilter),
                ("time_created", RangeDateFilter),
                ("owner", RelatedDropdownFilter),
            )
        return (
            ("category", RelatedDropdownFilter),
            ("time_created", RangeDateFilter),
        )

    @display(description="Фото")
    def get_thumbnail(self, obj):
        if not obj.photo:
            return "—"
        style = (
            "width:40px; height:40px; object-fit:cover; "
            "border-radius:8px; "
            "border:1px solid rgba(255,255,255,0.08);"
        )
        return format_html('<img src="{}" style="{}" />', obj.photo.url, style)

    @display(description="Превью")
    def get_photo_preview(self, obj):
        if not obj.photo:
            return "Фото ещё не загружено"
        style = (
            "width:160px; height:160px; object-fit:cover; "
            "border-radius:12px; "
            "border:1px solid rgba(255,255,255,0.08);"
        )
        return format_html('<img src="{}" style="{}" />', obj.photo.url, style)

    @display(description="Категория")
    def get_category_badge(self, obj):
        return badge(obj.category.cat, "#31572C", "#ECF39E")

    @display(description="Статус")
    def get_freshness_badge(self, obj):
        if not obj.pk:
            return "—"
        is_new = obj.time_created >= timezone.now() - timedelta(days=3)
        if is_new:
            return badge("Новинка", "#90A955", "#132A13")
        ago = timesince(obj.time_updated)
        return format_html(
            '<span style="color:rgba(255,255,255,0.55); '
            'font-size:12px;">обновлено {} назад</span>',
            ago,
        )

    @display(description="Статус товара")
    def get_status_badge_field(self, obj):
        if not obj.pk:
            return "Сохраните товар, чтобы увидеть статус"
        is_new = obj.time_created >= timezone.now() - timedelta(days=3)
        if is_new:
            return badge("Новинка", "#90A955", "#132A13")
        ago = timesince(obj.time_updated)
        return badge(f"Обновлено {ago}", "#33334a", "rgba(255,255,255,0.7)")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.owner = request.user
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser and "owner" in form.base_fields:
            form.base_fields["owner"].disabled = True
        return form

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category" and not request.user.is_superuser:
            kwargs["queryset"] = Categories.objects.filter(owner=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Categories)
class CategoriesAdmin(ModelAdmin):
    list_display = ("cat", "get_goods_count_badge", "owner")
    exclude = ["owner"]
    readonly_fields = ["get_goods_count_field"]
    fields = ("cat", "get_goods_count_field")
    warn_unsaved_form = True
    list_filter_sheet = True
    search_fields = ("cat",)

    @display(description="Товаров")
    def get_goods_count_badge(self, obj):
        count = obj.goods_set.count()
        if count > 0:
            return badge(count, "#4F772D", "#ECF39E")
        return badge(count, "#33334a", "rgba(255,255,255,0.55)")

    @display(description="Товаров в категории")
    def get_goods_count_field(self, obj):
        if not obj.pk:
            return "Сохраните категорию, чтобы увидеть количество товаров"
        return self.get_goods_count_badge(obj)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.owner = request.user
        super().save_model(request, obj, form, change)
