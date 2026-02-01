import pytest
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from apps.goodfood.models import Categories, Goods


@pytest.fixture(autouse=True, scope="session")
def disable_debug_toolbar():
    """Отключаем debug_toolbar во время тестов."""
    if "debug_toolbar" in settings.INSTALLED_APPS:
        settings.INSTALLED_APPS = tuple(
            app for app in settings.INSTALLED_APPS if app != "debug_toolbar"
        )


@pytest.fixture(autouse=True)
def media_root(tmp_path, settings):
    settings.MEDIA_ROOT = tmp_path


@pytest.fixture
def create_fake_image():
    return SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")


@pytest.fixture
def category():
    return Categories.objects.create(cat="category", id=999)


@pytest.fixture
def product(category, create_fake_image):
    return Goods.objects.create(
        name="product",
        category=category,
        photo=create_fake_image,
        slugify_name="slug",
        id=999,
    )


@pytest.fixture
def define_static_urls():
    urls = ["goodfood:main", "goodfood:goods"]
    defined_urls = []
    for url in urls:
        defined_urls.append(reverse(url))
    return defined_urls


@pytest.fixture
def define_dynamics_urls():
    urls = {
        "goodfood:_detail": {"kwargs": {"slug_name": "slug", "pk": 999}},
        "goodfood:_category": {"kwargs": {"cat_id": 999}},
    }
    defined_urls = []

    for name, params in urls.items():
        defined_urls.append(reverse(name, **params))
    return defined_urls


@pytest.fixture
def define_all_urls(define_static_urls, define_dynamics_urls):
    return define_static_urls + define_dynamics_urls
