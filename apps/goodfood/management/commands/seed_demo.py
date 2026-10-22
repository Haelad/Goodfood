"""Демо-аккаунт с рецептами, КБЖУ и дневником питания за последнюю неделю.

    python manage.py seed_demo          # создать (повторный запуск ничего не дублирует)
    python manage.py seed_demo --reset  # пересоздать демо-пользователя со всеми данными

Только для локальной разработки: логин и пароль ниже — тестовые.
"""

import random
from datetime import datetime, time, timedelta
from io import BytesIO
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from PIL import Image, ImageDraw, ImageFilter

from apps.goodfood.models import Categories, FoodEntry, Goods

DEMO_USERNAME = "demo"
DEMO_EMAIL = "demo@goodfood.local"
DEMO_PASSWORD = "demo-goodfood-2026"

PHOTOS_DIR = Path(__file__).resolve().parents[2] / "fixtures" / "demo_photos"

# Пищевая ценность на 100 г и обычная порция: ккал, белки, жиры, углеводы, г
NUTRITION = {
    "borscht": (55, 3.2, 2.4, 5.6, 350),
    "pumpkin": (62, 1.4, 3.1, 7.8, 300),
    "spinach": (95, 4.8, 6.9, 3.5, 200),
    "greek": (105, 3.4, 8.6, 4.2, 220),
    "syrniki": (220, 14.5, 9.8, 18.4, 180),
    "oatmeal": (110, 3.6, 2.9, 17.5, 250),
    "carbonara": (295, 12.1, 13.4, 31.2, 280),
    "teriyaki": (165, 11.8, 4.1, 20.6, 350),
    "charlotte": (210, 4.6, 3.9, 39.5, 120),
    "banana": (265, 4.3, 9.6, 41.8, 90),
}

# Что «съедено» по дням: завтрак, обед, ужин и иногда перекус
MEALS = [
    (time(8, 30), ("syrniki", "oatmeal")),
    (time(13, 15), ("borscht", "pumpkin", "teriyaki", "carbonara")),
    (time(19, 0), ("spinach", "greek", "teriyaki", "carbonara")),
    (time(16, 30), ("charlotte", "banana", None, None)),
]

# (категория, название, описание, фото из fixtures/demo_photos, цвета заглушки)
RECIPES = [
    (
        "Супы",
        "Борщ с говядиной",
        "Наваристый борщ на говяжьем бульоне со свёклой, капустой и картофелем.\n\n"
        "Свёклу тушите отдельно с томатной пастой и каплей уксуса — так цвет "
        "останется ярким. Подавайте со сметаной и чесночными пампушками.",
        "borscht",
        ("#7a1f2b", "#c2410c"),
    ),
    (
        "Супы",
        "Тыквенный крем-суп",
        "Нежный суп из запечённой тыквы с имбирём и сливками.\n\n"
        "Тыкву запекайте до карамельных краёв — это даёт глубину вкуса. "
        "Перед подачей добавьте обжаренные тыквенные семечки.",
        "pumpkin",
        ("#c2620c", "#f59e0b"),
    ),
    (
        "Салаты",
        "Салат со шпинатом и морковью",
        "Лёгкий салат из молодого шпината, тонкой моркови, фета и тыквенных "
        "семечек. Заправка — оливковое масло, лимонный сок и мёд.",
        "spinach",
        ("#2f5d1f", "#90a955"),
    ),
    (
        "Салаты",
        "Греческий салат",
        "Огурцы, помидоры, сладкий перец, красный лук, маслины и брынза.\n\n"
        "Не перемешивайте сыр с овощами — положите его сверху крупным куском "
        "и сбрызните маслом с орегано.",
        "greek",
        ("#3f6212", "#dc2626"),
    ),
    (
        "Завтраки",
        "Сырники со сметаной",
        "Пышные сырники из жирного творога с ванилью. Жарьте на среднем огне "
        "под крышкой, чтобы они пропеклись внутри и не подгорели.",
        "syrniki",
        ("#b45309", "#fde68a"),
    ),
    (
        "Завтраки",
        "Овсянка с ягодами",
        "Овсяная каша на молоке с черникой, малиной и ложкой мёда. "
        "Можно приготовить с вечера в банке и утром только разогреть.",
        "oatmeal",
        ("#6b21a8", "#e9d5ff"),
    ),
    (
        "Основные блюда",
        "Паста карбонара",
        "Спагетти с гуанчиале, желтками и пекорино — без сливок.\n\n"
        "Соус соединяйте с пастой вне огня, добавляя воду от варки, "
        "чтобы желтки не свернулись.",
        "carbonara",
        ("#a16207", "#fef3c7"),
    ),
    (
        "Основные блюда",
        "Курица терияки с рисом",
        "Куриные бёдра в соусе терияки с кунжутом и зелёным луком, "
        "к ним — рассыпчатый жасминовый рис.",
        "teriyaki",
        ("#78350f", "#f97316"),
    ),
    (
        "Выпечка",
        "Шарлотка с яблоками",
        "Классическая шарлотка из кислых яблок. Тесто — только яйца, сахар и "
        "мука, взбитые до пышности: секрет в долгом взбивании яиц.",
        "charlotte",
        ("#92400e", "#fcd34d"),
    ),
    ("Выпечка", "Банановый хлеб", "", "banana", ("#713f12", "#d6a75c")),
]


def recipe_photo(name, colors, seed):
    """Фото блюда из fixtures/demo_photos, если его нет — сгенерированная заглушка."""
    path = PHOTOS_DIR / f"{name}.jpg"
    if path.exists():
        return ContentFile(path.read_bytes())
    return plate_image(colors, seed)


def plate_image(colors, seed):
    """Заглушка фото: тёмный стол и «тарелка» с блюдом в его цветах."""
    rnd = random.Random(seed)
    width, height = 1200, 900
    img = Image.new("RGB", (width, height), "#16141f")
    draw = ImageDraw.Draw(img)

    cx, cy, r = width // 2 + rnd.randint(-80, 80), height // 2, 330
    draw.ellipse((cx - r - 30, cy - r - 30, cx + r + 30, cy + r + 30), fill="#2a2838")
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=colors[0])
    for _ in range(40):
        x = cx + rnd.randint(-r + 60, r - 60)
        y = cy + rnd.randint(-r + 60, r - 60)
        s = rnd.randint(18, 60)
        draw.ellipse((x - s, y - s, x + s, y + s), fill=colors[rnd.randint(0, 1)])

    img = img.filter(ImageFilter.GaussianBlur(6))
    buffer = BytesIO()
    img.save(buffer, format="JPEG", quality=85)
    return ContentFile(buffer.getvalue())


class Command(BaseCommand):
    help = "Создаёт демо-аккаунт с рецептами для локальной проверки вёрстки"

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="удалить и создать заново рецепты и категории демо-аккаунта",
        )

    def handle(self, *args, reset, **options):
        if not settings.DEBUG:
            raise CommandError("seed_demo предназначен только для DEBUG=True")

        User = get_user_model()
        if reset:
            # сначала рецепты (вместе с записями дневника): категория у товара
            # защищена PROTECT, поэтому каскад от пользователя на них упадёт
            Goods.objects.filter(owner__username=DEMO_USERNAME).delete()
            User.objects.filter(username=DEMO_USERNAME).delete()

        user = User.objects.filter(username=DEMO_USERNAME).first()
        if user is not None:
            self.stdout.write(
                "Демо-аккаунт уже есть — запустите с --reset, чтобы пересоздать"
            )
            return

        # сигнал выдаст права и создаст «Без категории»
        user = User.objects.create_user(DEMO_USERNAME, DEMO_EMAIL, DEMO_PASSWORD)

        now = timezone.now()
        by_photo = {}
        for index, (cat, name, desc, photo, colors) in enumerate(RECIPES):
            category = Categories.get_or_create_for(user, cat)
            kcal, proteins, fats, carbs, portion = NUTRITION[photo]
            goods = Goods(
                owner=user,
                name=name,
                desc=desc or None,
                category=category,
                kcal=kcal,
                proteins=proteins,
                fats=fats,
                carbs=carbs,
                portion_grams=portion,
            )
            goods.photo.save(
                f"demo-{photo}.jpg", recipe_photo(photo, colors, index), save=False
            )
            goods.save()
            # разные даты, чтобы список и «Новинка» выглядели правдоподобно
            created = now - timedelta(days=index * 4 + 1, hours=index)
            Goods.objects.filter(pk=goods.pk).update(
                time_created=created, time_updated=created + timedelta(days=index % 3)
            )
            by_photo[photo] = goods

        entries = self.fill_diary(user, by_photo)
        self.stdout.write(
            self.style.SUCCESS(
                f"Готово. Рецептов: {len(RECIPES)}, записей дневника: {entries}"
            )
        )

    def fill_diary(self, user, by_photo):
        """Записи за последние 7 дней; сегодня — только то, что уже «прошло»."""
        rnd = random.Random(42)
        now = timezone.localtime()
        entries = []
        for offset in range(6, -1, -1):
            day = now.date() - timedelta(days=offset)
            for meal_time, options in MEALS:
                photo = rnd.choice(options)
                eaten_at = timezone.make_aware(datetime.combine(day, meal_time))
                if photo is None or eaten_at > now:
                    continue
                goods = by_photo[photo]
                grams = round(goods.portion_grams * rnd.uniform(0.8, 1.2) / 10) * 10
                entries.append(
                    FoodEntry(owner=user, goods=goods, grams=grams, eaten_at=eaten_at)
                )
        FoodEntry.objects.bulk_create(entries)
        return len(entries)
