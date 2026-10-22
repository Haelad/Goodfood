from django import forms
from django.core.validators import MaxLengthValidator
from unfold.widgets import UnfoldAdminTextInputWidget

from .models import Categories, Goods
from .validators import GoodfoodValidator


class GoodsAdminForm(forms.ModelForm):
    """Форма рецепта: категорию можно выбрать или сразу вписать новую.

    Если не сделано ни то ни другое, рецепт попадает в «Без категории».
    Саму категорию назначает GoodsAdmin.save_model — там известен пользователь.
    """

    new_category = forms.CharField(
        label="Или новая категория",
        required=False,
        max_length=32,
        validators=[MaxLengthValidator(32), GoodfoodValidator()],
        widget=UnfoldAdminTextInputWidget(attrs={"placeholder": "Например: Супы"}),
        help_text="Впишите название — категория создастся при сохранении",
    )

    class Meta:
        model = Goods
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        category = self.fields.get("category")
        if category:
            category.required = False
            category.help_text = "Не выбрали — рецепт попадёт в «Без категории»"

    def clean_new_category(self):
        return self.cleaned_data["new_category"].strip()

    def resolve_category(self, owner):
        """Итоговая категория: новая → выбранная → «Без категории»."""
        new_name = self.cleaned_data.get("new_category")
        if new_name:
            return Categories.get_or_create_for(owner, new_name)
        return self.cleaned_data.get("category") or Categories.default_for(owner)
