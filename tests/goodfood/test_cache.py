import pytest
from django.conf import settings
from django.core.cache import cache, caches


def test_cache_connection():
    result = cache.set("debug_key", "hello", timeout=60)
    print("set result:", result)
    print("get result:", cache.get("debug_key"))
    print("backend:", cache.__class__)
    print("CACHES:", settings.CACHES)
    print("Backend:", caches["default"].__class__)


@pytest.mark.django_db
def test_cache_set_list(
    authenticated_client, unauthenticated_client, products, categories, define_all_urls
):
    user_id = unauthenticated_client.pk

    product = products[0]
    category = categories[0]

    for url in define_all_urls:
        response = authenticated_client.get(url)
        assert response.status_code == 200

    cache_keys = [
        f"goods:food:user:{user_id}",
        f"goods:detail-food:user:{user_id}:pk:{product.pk}",
        f"goods:category-food:user:{user_id}:cat_id:{category.pk}",
    ]

    for key in cache_keys:
        assert cache.get(key) is not None
