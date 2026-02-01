import pytest
from pytest_django.asserts import assertContains


@pytest.mark.django_db
def test_if_view_recive_model(category, product, client, define_all_urls):
    for url in define_all_urls:
        response = client.get(url)
        assert response.status_code == 200

    assertContains(response, category.cat)
    assertContains(response, product.name)
