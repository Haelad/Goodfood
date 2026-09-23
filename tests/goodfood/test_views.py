import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains

from apps.goodfood.models import Goods


@pytest.mark.django_db
def test_index_view_head_returns_200(
    categories, products, authenticated_client, define_all_urls
):
    for url in define_all_urls:
        head_response = authenticated_client.head(url)
        assert head_response.status_code == 200

    for url in define_all_urls:
        get_response = authenticated_client.get(url)
        assert get_response.status_code == 200

    list_response = authenticated_client.get(reverse("goodfood:goods"))
    assert list_response.status_code == 200
    for product in Goods.objects.order_by("-time_created")[:12]:
        assertContains(list_response, product.name)

    for product in products:
        detail_response = authenticated_client.get(product.get_absolute_url())
        assert detail_response.status_code == 200
        assertContains(detail_response, product.name)
