from io import BytesIO

import pytest
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from apps.goodfood.models import DEFAULT_CATEGORY_NAME, Categories, Goods

ADD_URL = "/admin/goodfood/goods/add/"


def png_file():
    # Настоящий PNG: validate_image_file проверяет MIME через libmagic
    buffer = BytesIO()
    Image.new("RGB", (10, 10), "green").save(buffer, format="PNG")
    return SimpleUploadedFile("dish.png", buffer.getvalue(), content_type="image/png")


@pytest.fixture
def cook(db):
    return User.objects.create_user(username="cook", password="test_user_42")


@pytest.fixture
def cook_client(client, cook):
    client.force_login(cook)
    return client


def post_recipe(client, **extra):
    data = {"name": "Борщ", "desc": "Свекольный суп", "photo": png_file(), **extra}
    return client.post(ADD_URL, data)


def test_signup_creates_default_category(cook):
    assert Categories.objects.filter(owner=cook, cat=DEFAULT_CATEGORY_NAME).count() == 1


def test_add_form_preselects_default_category(cook_client, cook):
    default = Categories.objects.get(owner=cook, cat=DEFAULT_CATEGORY_NAME)

    response = cook_client.get(ADD_URL)

    assert response.context["adminform"].form.initial["category"] == default.pk


def test_recipe_without_category_goes_to_default(cook_client, cook):
    response = post_recipe(cook_client)

    assert response.status_code == 302
    assert Goods.objects.get(owner=cook).category.cat == DEFAULT_CATEGORY_NAME


def test_new_category_is_created_from_recipe_form(cook_client, cook):
    response = post_recipe(cook_client, new_category="  Супы ")

    assert response.status_code == 302
    category = Goods.objects.get(owner=cook).category
    assert category.cat == "Супы"
    assert category.owner == cook


def test_new_category_reuses_existing_case_insensitive(cook_client, cook):
    soups = Categories.objects.create(owner=cook, cat="Супы")

    post_recipe(cook_client, new_category="супы")

    assert Goods.objects.get(owner=cook).category == soups
    assert Categories.objects.filter(owner=cook, cat__iexact="супы").count() == 1


def test_new_category_wins_over_selected(cook_client, cook):
    salads = Categories.objects.create(owner=cook, cat="Салаты")

    post_recipe(cook_client, category=salads.pk, new_category="Супы")

    assert Goods.objects.get(owner=cook).category.cat == "Супы"


def test_new_category_is_validated(cook_client, cook):
    response = post_recipe(cook_client, new_category="<script>")

    assert response.status_code == 200
    assert "new_category" in response.context["adminform"].form.errors
    assert not Goods.objects.filter(owner=cook).exists()
