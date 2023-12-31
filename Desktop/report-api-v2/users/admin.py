import logging

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from .models import User

logger = logging.getLogger(__name__)


class UserAdmin(BaseUserAdmin):
    ordering = ["id"]
    list_display = ["mkanid", "name"]
    fieldsets = (
        (None, {"fields": ("mkanid", "password")}),
        (_("Personal Info"), {"fields": ("name",)}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser")}),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("mkanid", "password1", "password2")}),
    )


admin.site.register(User, UserAdmin)
