from datetime import timedelta
from decimal import Decimal

import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from apps.goodfood.models import Categories, FoodEntry, Goods


@pytest.fixture
def cook(db):
    return User.objects.create_user(username="cook", password="test_user_42")


@pytest.fixture
def cook_client(client, cook):
    client.force_login(cook)
    return client


@pytest.fixture
def soup(cook):
    category = Categories.default_for(cook)
    return Goods.objects.create(
        owner=cook,
        name="Борщ",
        photo="goods/borscht.jpg",
        category=category,
        kcal=Decimal("55"),
        proteins=Decimal("3.2"),
        fats=Decimal("2.4"),
        carbs=Decimal("5.6"),
        portion_grams=350,
    )


def test_entry_scales_nutrition_by_weight(cook, soup):
    entry = FoodEntry.objects.create(owner=cook, goods=soup, grams=300)

    assert entry.kcal == Decimal("165")
    assert entry.nutrient("proteins") == Decimal("10")


def test_entry_without_nutrition_has_no_kcal(cook, soup):
    soup.kcal = None
    soup.save()
    entry = FoodEntry.objects.create(owner=cook, goods=soup, grams=300)

    assert entry.kcal is None


def test_totals_sum_entries(cook, soup):
    FoodEntry.objects.create(owner=cook, goods=soup, grams=200)
    FoodEntry.objects.create(owner=cook, goods=soup, grams=100)

    totals = FoodEntry.objects.filter(owner=cook).totals()

    assert totals["kcal"] == Decimal("165")
    assert totals["carbs"] == Decimal("17")


def test_totals_of_empty_queryset_are_zero(db):
    assert FoodEntry.objects.none().totals()["kcal"] == Decimal("0")


def test_log_eaten_prefills_goods_and_portion(cook_client, soup):
    url = reverse("admin:goodfood_goods_log_eaten", args=[soup.pk])

    response = cook_client.get(url)

    assert response.status_code == 302
    assert response.url.endswith(f"?goods={soup.pk}&grams=350")
    form = cook_client.get(response.url).context["adminform"].form
    assert form.initial["grams"] == "350"


def test_diary_changelist_filters_today_and_shows_totals(cook_client, cook, soup):
    FoodEntry.objects.create(owner=cook, goods=soup, grams=200)
    FoodEntry.objects.create(
        owner=cook, goods=soup, grams=500, eaten_at=timezone.now() - timedelta(days=3)
    )

    response = cook_client.get(
        reverse("admin:goodfood_foodentry_changelist") + "?period=today"
    )

    assert response.status_code == 200
    assert response.context["cl"].result_count == 1
    assert "110 ккал" in response.content.decode()


def test_diary_is_private(client, cook, soup):
    FoodEntry.objects.create(owner=cook, goods=soup, grams=200)
    other = User.objects.create_user(username="other", password="test_user_42")
    client.force_login(other)

    response = client.get(reverse("admin:goodfood_foodentry_changelist"))

    assert response.context["cl"].result_count == 0


def test_dashboard_shows_today_kcal(cook_client, cook, soup):
    FoodEntry.objects.create(owner=cook, goods=soup, grams=200)

    response = cook_client.get(reverse("admin:index"))

    assert response.status_code == 200
    assert response.context["kpi"][0]["value"] == "110 ккал"


def test_navbar_lists_only_non_empty_categories(cook_client, cook, soup):
    Categories.objects.create(owner=cook, cat="Пустая")

    response = cook_client.get(reverse("goodfood:main"))

    names = [c.cat for c in response.context["nav_categories"]]
    assert names == [soup.category.cat]


def test_eat_logs_portion_and_returns_today_state(cook_client, cook, soup):
    response = cook_client.post(reverse("goodfood:eat", args=[soup.pk]))

    assert response.status_code == 200
    entry = FoodEntry.objects.get(owner=cook)
    assert entry.grams == soup.portion_grams
    data = response.json()
    assert data["count"] == 1
    assert data["totals"]["kcal"] == "192"  # 55 ккал × 350 г / 100


def test_eat_twice_counts_twice(cook_client, soup):
    url = reverse("goodfood:eat", args=[soup.pk])
    cook_client.post(url)

    assert cook_client.post(url).json()["count"] == 2


def test_uneat_removes_only_latest_today_entry(cook_client, cook, soup):
    yesterday = timezone.now() - timedelta(days=1)
    FoodEntry.objects.create(owner=cook, goods=soup, grams=100, eaten_at=yesterday)
    cook_client.post(reverse("goodfood:eat", args=[soup.pk]))

    response = cook_client.post(reverse("goodfood:uneat", args=[soup.pk]))

    assert response.json()["count"] == 0
    assert FoodEntry.objects.filter(owner=cook).count() == 1  # вчерашняя осталась


def test_uneat_with_nothing_today_is_harmless(cook_client, soup):
    response = cook_client.post(reverse("goodfood:uneat", args=[soup.pk]))

    assert response.status_code == 200
    assert response.json()["count"] == 0


def test_eat_requires_post(cook_client, soup):
    response = cook_client.get(reverse("goodfood:eat", args=[soup.pk]))

    assert response.status_code == 405


def test_cannot_eat_someone_elses_goods(client, soup):
    other = User.objects.create_user(username="other", password="test_user_42")
    client.force_login(other)

    response = client.post(reverse("goodfood:eat", args=[soup.pk]))

    assert response.status_code == 404
    assert not FoodEntry.objects.exists()


def test_list_marks_today_count_on_cards(cook_client, cook, soup):
    FoodEntry.objects.create(owner=cook, goods=soup, grams=100)
    FoodEntry.objects.create(owner=cook, goods=soup, grams=100)

    response = cook_client.get(reverse("goodfood:goods"))

    card = next(g for g in response.context["object_list"] if g.pk == soup.pk)
    assert card.today_count == 2
    assert response.context["today_totals"]["kcal"] == Decimal("110")
