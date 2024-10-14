from typing import Any

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from routine_tracker.accounts.models import User, UserProfile


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("password",)}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("usable_password", "password1", "password2"),
            },
        ),
    )
    list_display = ("email", "first_name", "last_name", "is_staff")
    search_fields = ("first_name", "last_name", "email")
    ordering = ("email",)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'dark_mode', 'preferred_language', 'time_zone')
    list_filter = ('dark_mode', 'preferred_language', 'time_zone')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    raw_id_fields = ('user',)
    list_select_related = ('user',)
    fieldsets = (
        (None, {'fields': ('user',)}),
        ('Preferences', {'fields': ('dark_mode', 'preferred_language', 'time_zone')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('user', 'dark_mode', 'preferred_language', 'time_zone'),
            },
        ),
    )

    def get_readonly_fields(self, _, obj: Any | None = ...) -> list[str] | tuple[Any, ...]:
        # Make the user field "create"-only
        if obj:
            return ('user',)
        return ()
