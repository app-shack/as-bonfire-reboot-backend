from django.contrib import admin

from . import models


@admin.register(models.MassageQueueEntry)
class MassageQueueEntryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "status",
        "queue_position",
    )
    fields = (
        "created_at",
        "updated_at",
        "user",
        "status",
        "queue_position",
    )
    readonly_fields = ("created_at", "updated_at", "user", "status", "queue_position")

    def get_queryset(self, request):
        return models.MassageQueueEntry.objects.order_by(
            "-created_at",
            "queue_position",
        )
