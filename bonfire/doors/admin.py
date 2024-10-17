from django.contrib import admin

from . import models


@admin.register(models.Door)
class DoorAdmin(admin.ModelAdmin):
    list_display = ("slug", "status")
    fields = (
        "created_at",
        "updated_at",
        "status",
        "slug",
        "output_number",
        "external_id",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "status",
    )


@admin.register(models.DoorLog)
class DoorLogAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "get_door_slug",
        "status",
    )
    fields = (
        "created_at",
        "get_door_slug",
        "user_email",
        "user_first_name",
        "user_last_name",
    )
    readonly_fields = fields

    ordering = ("-created_at",)

    def get_queryset(self, request):
        return models.DoorLog.objects.select_related("door")

    def get_door_slug(self, obj):
        return obj.door.slug
