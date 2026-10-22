import uuid
from datetime import datetime, time, timedelta
from decimal import Decimal

from django.conf import settings
from django.core.validators import (
    MaxLengthValidator,
    MaxValueValidator,
    MinLengthValidator,
    MinValueValidator,
    RegexValidator,
)
from django.db import models
from django.db.models import DecimalField, ExpressionWrapper, F, Sum
from django.urls import reverse
from django.utils import timezone
from slugify import slugify

from apps.goodfood.validators import GoodfoodValidator, validate_image_file

DEFAULT_CATEGORY_NAME = "Без категории"


class Categories(models.Model):
    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name="Владелец",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    cat = models.CharField(
        verbose_name="категория",
        max_length=32,
        db_index=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(32), GoodfoodValidator()],
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.cat

    def get_absolute_url(self):
        return reverse("goodfood:_category", kwargs={"cat_id": self.pk})

    @classmethod
    def get_or_create_for(cls, owner, name):
        """Категория пользователя по названию (без учёта регистра) или новая."""
        name = name.strip()
        category = cls.objects.filter(owner=owner, cat__iexact=name).first()
        if category is None:
            category = cls.objects.create(owner=owner, cat=name)
        return category

    @classmethod
    def default_for(cls, owner):
        return cls.get_or_create_for(owner, DEFAULT_CATEGORY_NAME)


def nutrition_field(verbose_name, max_value=100):
    return models.DecimalField(
        verbose_name=verbose_name,
        max_digits=5,
        decimal_places=1,
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(max_value)],
        help_text="на 100 г",
    )


def upload_to(instance, filename):
    ext = filename.split(".")[-1]
    return f"goods/{uuid.uuid4()}.{ext}"


class Goods(models.Model):
    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name="Владелец",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    name = models.CharField(
        verbose_name="Название",
        max_length=64,
        db_index=True,
        editable=True,
        validators=[MinLengthValidator(1), MaxLengthValidator(64), GoodfoodValidator()],
    )

    photo = models.ImageField(
        verbose_name="Фото",
        name="photo",
        blank=False,
        null=False,
        editable=True,
        upload_to=upload_to,
        validators=[validate_image_file],
    )

    description = models.TextField(
        verbose_name="Описание",
        name="desc",
        max_length=256,
        unique=False,
        blank=True,
        null=True,
        editable=True,
        validators=[
            MinLengthValidator(1),
            MaxLengthValidator(256),
            GoodfoodValidator(),
        ],
    )

    category = models.ForeignKey(
        to=Categories,
        verbose_name="категория",
        name="category",
        on_delete=models.PROTECT,
    )

    slugify_name = models.SlugField(
        max_length=256,
        blank=True,
        unique=True,
        allow_unicode=True,
        verbose_name="Слаг",
        validators=[
            RegexValidator(
                regex=r"^[-a-zA-Z0-9_]+$",
                message="Slug может содержать только буквы,\
                    цифры, дефис и подчёркивания.",
            )
        ],
    )

    # Пищевая ценность на 100 г — как на упаковке. Необязательна, чтобы
    # старые записи и блюда «на глаз» не ломали форму.
    kcal = nutrition_field("Калории, ккал", max_value=900)
    proteins = nutrition_field("Белки, г")
    fats = nutrition_field("Жиры, г")
    carbs = nutrition_field("Углеводы, г")
    portion_grams = models.PositiveIntegerField(
        verbose_name="Обычная порция, г",
        # db_default — чтобы код из других веток мог вставлять товары в эту же БД
        default=100,
        db_default=100,
        validators=[MinValueValidator(1), MaxValueValidator(5000)],
        help_text="Подставляется по умолчанию, когда записываете, что съели",
    )

    time_created = models.DateTimeField(
        verbose_name="Время создания", auto_now_add=True, editable=False
    )
    time_updated = models.DateTimeField(
        verbose_name="Время изменения", auto_now=True, editable=True
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

        db_table_comment = "База данных с рецептами блюд"

        ordering = ["-time_created"]

        get_latest_by = ["time_updated"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slugify_name:
            self.slugify_name = slugify(self.name)
        super(Goods, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "goodfood:_detail", kwargs={"slug_name": self.slugify_name, "pk": self.pk}
        )


NUTRIENTS = ("kcal", "proteins", "fats", "carbs")


class FoodEntryQuerySet(models.QuerySet):
    def today(self):
        """Записи за сегодняшний день по TIME_ZONE проекта."""
        start = timezone.make_aware(datetime.combine(timezone.localdate(), time.min))
        return self.filter(eaten_at__gte=start, eaten_at__lt=start + timedelta(days=1))

    def totals(self):
        """Сумма калорий и БЖУ по записям: значение на 100 г × граммы / 100."""
        output = DecimalField(max_digits=10, decimal_places=1)
        sums = self.aggregate(
            **{
                name: Sum(
                    ExpressionWrapper(
                        F(f"goods__{name}") * F("grams") / 100, output_field=output
                    )
                )
                for name in NUTRIENTS
            }
        )
        return {
            name: (value or Decimal(0)).quantize(Decimal("1"))
            for name, value in sums.items()
        }


class FoodEntry(models.Model):
    """Запись дневника питания: что, сколько и когда съедено."""

    owner = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        verbose_name="Владелец",
        on_delete=models.CASCADE,
    )
    goods = models.ForeignKey(
        to=Goods,
        verbose_name="Что съели",
        on_delete=models.CASCADE,
        related_name="entries",
    )
    grams = models.PositiveIntegerField(
        verbose_name="Сколько, г",
        validators=[MinValueValidator(1), MaxValueValidator(5000)],
    )
    eaten_at = models.DateTimeField(
        verbose_name="Когда", default=timezone.now, db_index=True
    )

    objects = FoodEntryQuerySet.as_manager()

    class Meta:
        verbose_name = "Запись дневника"
        verbose_name_plural = "Дневник питания"
        ordering = ["-eaten_at"]

    def __str__(self):
        return f"{self.goods} — {self.grams} г"

    def nutrient(self, name):
        """Значение нутриента для съеденного веса или None, если не указано."""
        per_100 = getattr(self.goods, name)
        if per_100 is None:
            return None
        return (per_100 * self.grams / 100).quantize(Decimal("1"))

    @property
    def kcal(self):
        return self.nutrient("kcal")
