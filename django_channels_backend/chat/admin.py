from django.contrib import admin

# Register your models here.
from chat.models import User

from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _
@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "group_name",
                )
            },
        ),

        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),

    )
    list_display = ["id", "email", "username", "is_superuser"]
    search_fields = ["email"]