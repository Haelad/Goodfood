import pytest
from django.conf import settings
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from factorytest import CategoryFactory, GoodsFactory


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
def categories(db):
    return CategoryFactory.create_batch(10)


@pytest.fixture
def products(db, categories):
    products = []
    for category in categories:
        products.extend(GoodsFactory.create_batch(3, category=category))
    return products


@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()


@pytest.fixture
def define_static_urls():
    urls = ["goodfood:main", "goodfood:goods"]
    defined_urls = []
    for url in urls:
        defined_urls.append(reverse(url))
    return defined_urls


@pytest.fixture
def define_dynamics_urls(products, categories):
    defined_urls = []
    detail_kwargs = {"kwargs": {"slug_name": "", "pk": ""}}
    for product in products:
        detail_kwargs["kwargs"]["slug_name"] = product.slugify_name
        detail_kwargs["kwargs"]["pk"] = product.pk
        defined_urls.append(reverse("goodfood:_detail", kwargs=detail_kwargs["kwargs"]))

    category_kwargs = {"kwargs": {"cat_id": ""}}
    for category in categories:
        category_kwargs["kwargs"]["cat_id"] = category.pk
        defined_urls.append(
            reverse("goodfood:_category", kwargs=category_kwargs["kwargs"])
        )

    return defined_urls


@pytest.fixture
def define_all_urls(define_static_urls, define_dynamics_urls):
    return define_static_urls + define_dynamics_urls
