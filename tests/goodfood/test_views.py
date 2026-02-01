import pytest


@pytest.mark.django_db
def test_index_view_head_returns_200(category, product, client, define_all_urls):
    for url in define_all_urls:
        response = client.head(url)
        assert response.status_code == 200
