import pytest
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_new_user_gets_staff_and_goods_permissions():
    user = User.objects.create_user(username="new_cook", password="test_user_42")
    user = User.objects.get(pk=user.pk)  # сигнал меняет is_staff через update()

    assert user.is_staff
    assert user.has_perms(
        [
            "goodfood.add_goods",
            "goodfood.change_goods",
            "goodfood.delete_goods",
            "goodfood.view_goods",
            "goodfood.add_categories",
            "goodfood.change_categories",
            "goodfood.delete_categories",
            "goodfood.view_categories",
            "goodfood.add_foodentry",
            "goodfood.change_foodentry",
            "goodfood.delete_foodentry",
            "goodfood.view_foodentry",
        ]
    )


@pytest.mark.django_db
def test_superuser_permissions_untouched():
    admin = User.objects.create_superuser(username="boss", password="test_user_42")

    assert not admin.user_permissions.exists()


@pytest.mark.django_db
def test_new_user_can_open_goods_add_page(client):
    user = User.objects.create_user(username="new_cook", password="test_user_42")
    client.force_login(user)

    response = client.get("/admin/goodfood/goods/add/")

    assert response.status_code == 200
