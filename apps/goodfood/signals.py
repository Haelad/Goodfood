import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.core.cache import cache
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from .models import Categories, Goods

logger = logging.getLogger(__name__)

User = get_user_model()


@receiver(post_save, sender=User)
def set_user_permissions(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:
        User.objects.filter(pk=instance.pk).update(is_staff=True)

        permissions = Permission.objects.filter(
            codename__in=[
                "add_goods",
                "change_goods",
                "delete_goods",
                "view_goods",
                "add_categories",
                "change_categories",
                "delete_categories",
                "view_categories",
            ]
        )
        instance.user_permissions.set(permissions)


@receiver(pre_save, sender=Goods)
def save_old_goods_values(sender, instance, **kwargs):
    if instance.pk:
        old_goods = sender.objects.get(pk=instance.pk)

        instance._old_owner_id = old_goods.owner_id
        instance._old_category_id = old_goods.category_id


@receiver(post_save, sender=Goods)
def invalidate_goods_cache(sender, instance, **kwargs):
    # Старые значения
    old_owner_id = getattr(instance, "_old_owner_id", None)
    old_category_id = getattr(instance, "_old_category_id", None)

    if old_owner_id is not None:
        cache.delete(f"goods:food:user:{old_owner_id}")
        cache.delete(f"goods:detail-food:user:{old_owner_id}:pk:{instance.pk}")

        if old_category_id is not None:
            cache.delete(
                f"goods:category-food:user:{old_owner_id}:cat_id:{old_category_id}"
            )

    # Новые значения
    cache.delete(f"goods:food:user:{instance.owner_id}")
    cache.delete(f"goods:detail-food:user:{instance.owner_id}:pk:{instance.pk}")
    cache.delete(
        f"goods:category-food:user:{instance.owner_id}:cat_id:{instance.category_id}"
    )


@receiver(post_delete, sender=Goods)
def invalidate_goods_cache_on_delete(sender, instance, **kwargs):
    cache.delete(f"goods:food:user:{instance.owner_id}")
    cache.delete(f"goods:detail-food:user:{instance.owner_id}:pk:{instance.pk}")
    cache.delete(
        f"goods:category-food:user:{instance.owner_id}:cat_id:{instance.category_id}"
    )


@receiver(pre_save, sender=Categories)
def save_old_category_values(sender, instance, **kwargs):
    if instance.pk:
        old_category = sender.objects.get(pk=instance.pk)
        instance._old_owner_id = old_category.owner_id


@receiver(post_save, sender=Categories)
def invalidate_category_cache(sender, instance, **kwargs):
    old_owner_id = getattr(instance, "_old_owner_id", None)

    if old_owner_id is not None:
        cache.delete(f"goods:category-food:user:{old_owner_id}:cat_id:{instance.pk}")

    cache.delete(f"goods:category-food:user:{instance.owner_id}:cat_id:{instance.pk}")


@receiver(post_delete, sender=Categories)
def invalidate_category_cache_on_delete(sender, instance, **kwargs):
    cache.delete(f"goods:category-food:user:{instance.owner_id}:cat_id:{instance.pk}")
