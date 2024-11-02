from django.contrib import admin

from .models import Routine, RoutineEntry, RoutineGroup


class RoutineEntryInline(admin.TabularInline):
    model = RoutineEntry
    extra = 0
    fields = ("date", "value")
    ordering = ("-date",)
    show_change_link = True


class RoutineInline(admin.TabularInline):
    model = Routine
    extra = 0
    fields = ("name", "type", "goal")
    ordering = ("name",)
    show_change_link = True


@admin.register(RoutineGroup)
class RoutineGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "color")
    list_filter = ("user", "color")
    search_fields = ("name", "description")
    ordering = ("name",)
    raw_id_fields = ("user",)
    list_select_related = ("user",)
    fieldsets = (
        (None, {"fields": ("user", "name", "description")}),
        ("Visuals", {"fields": ("icon", "color")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("user", "name", "description", "icon", "color"),
            },
        ),
    )
    inlines = (RoutineInline,)


@admin.register(Routine)
class RoutineAdmin(admin.ModelAdmin):
    list_display = ("name", "group", "type", "goal")
    list_filter = ("group", "type")
    search_fields = ("name", "description")
    ordering = ("name",)
    raw_id_fields = ("group",)
    list_select_related = ("group",)
    fieldsets = (
        (None, {"fields": ("group", "name", "description")}),
        ("Visuals", {"fields": ("icon",)}),
        ("Goal", {"fields": ("type", "has_goal", "goal", "measure")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("group", "name", "description", "icon", "type", "goal", "measure"),
            },
        ),
    )
    inlines = (RoutineEntryInline,)
