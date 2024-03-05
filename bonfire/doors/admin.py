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
