from django.contrib import admin
from django.utils.html import format_html


class GetImageNormalMixin:
    IMAGE_HEIGHT_PX = 150

    @admin.display(description="Image")
    def get_image(self, obj):
        if not obj.original:
            return ""
        if not obj.normal:
            return "loading..."

        url = obj.normal.url
        return format_html(
            '<img src="{}" width="auto" height="{}px" />', url, self.IMAGE_HEIGHT_PX
        )


class GetImageNormal150PXMixin(GetImageNormalMixin):
    IMAGE_HEIGHT_PX = 150


class GetImageNormal64PXMixin(GetImageNormalMixin):
    IMAGE_HEIGHT_PX = 64
