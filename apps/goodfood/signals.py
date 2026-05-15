from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.db.models.signals import post_save
from django.dispatch import receiver

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
