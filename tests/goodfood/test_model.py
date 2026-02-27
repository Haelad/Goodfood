import pytest
from django.urls import reverse
from pytest_django.asserts import assertContains

from apps.goodfood.models import Goods


@pytest.mark.django_db
def test_if_view_recife_model(categories, products, client, define_static_urls):
    for url in define_static_urls:
        response = client.get(url)
        assert response.status_code == 200

    goods_response = client.get(reverse("goodfood:goods"))
    assert goods_response.status_code == 200
    for product in Goods.objects.order_by("-time_created")[:12]:
        assertContains(goods_response, product.name)
