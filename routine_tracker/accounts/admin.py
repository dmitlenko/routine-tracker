from typing import Any

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from routine_tracker.accounts.models import User, UserProfile

admin.site.register(User, UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'dark_mode', 'preferred_language', 'time_zone')
    list_filter = ('dark_mode', 'preferred_language', 'time_zone')
    search_fields = ('user__username', 'user__email')
    ordering = ('user__username',)
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
