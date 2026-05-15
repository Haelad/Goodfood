from django.contrib import admin

from .models import Categories, Goods


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    empty_value_display = "-пусто-"
    readonly_fields = ["time_created", "time_updated"]
    fieldsets = (
        (
            "",
            {
                "classes": ["wide"],
                "fields": ("name", "desc", "category"),
                "description": "[Обязательно] Укажите все поля, \
                    пользуйтесь кириллицей или латиницей",
            },
        ),
        (
            "Фото",
            {
                "fields": ("photo",),
                "description": "[Обязательно] Укажите поле фото размером 100 x 100",
            },
        ),
        (
            "Информация для администратора",
            {
                "classes": ["collapse"],
                "fields": (
                    "slugify_name",
                    ("time_created", "time_updated"),
                ),
            },
        ),
    )
    search_fields = ("name",)
    list_filter = ("category__cat",)
    warn_unsaved_form = True
    list_filter_sheet = True

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
class CategoriesAdmin(admin.ModelAdmin):
    exclude = ["owner"]
    warn_unsaved_form = True
    search_fields = ("cat",)
    list_filter = ("cat",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.owner = request.user
        super().save_model(request, obj, form, change)
