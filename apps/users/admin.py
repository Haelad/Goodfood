"""Перерегистрация стандартных моделей (auth, sites, allauth) в стиле unfold.

apps.users стоит в INSTALLED_APPS раньше django.contrib.* и allauth, поэтому
их admin-модули импортируются здесь явно: так модели уже зарегистрированы
к моменту unregister().
"""

from allauth.account import admin as account_admin
from allauth.socialaccount import admin as socialaccount_admin
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.models import Group, User
from django.contrib.sites import admin as sites_admin
from django.contrib.sites.models import Site
from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm


def reregister(model, base_admin):
    """Заменяет стандартный ModelAdmin на версию с unfold.ModelAdmin."""
    if not admin.site.is_registered(model):
        return
    admin.site.unregister(model)
    admin_class = type(base_admin.__name__, (base_admin, ModelAdmin), {})
    admin.site.register(model, admin_class)


admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin, ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "date_joined",
    )
    list_filter_sheet = True
    compressed_fields = True
    warn_unsaved_form = True


@admin.register(Group)
class GroupAdmin(auth_admin.GroupAdmin, ModelAdmin):
    pass


reregister(Site, sites_admin.SiteAdmin)
reregister(account_admin.EmailAddress, account_admin.EmailAddressAdmin)
reregister(account_admin.EmailConfirmation, account_admin.EmailConfirmationAdmin)
reregister(socialaccount_admin.SocialApp, socialaccount_admin.SocialAppAdmin)
reregister(socialaccount_admin.SocialAccount, socialaccount_admin.SocialAccountAdmin)
reregister(socialaccount_admin.SocialToken, socialaccount_admin.SocialTokenAdmin)
