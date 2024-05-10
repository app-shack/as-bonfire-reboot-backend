import uuid

from django.db import models, transaction
from django.utils import timezone
from PIL import Image, ImageOps

from utils.image import pil_to_django_image


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)

    class Meta:
        abstract = True


class ImageResizeMixIn(models.Model):
    _post_process_task = None
    _image_config = {}

    __previous_original = None

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__previous_original = self.original

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        original_image_changed = self.original != self.__previous_original
        if original_image_changed or is_new:
            self.__previous_original = self.original
            if self._post_process_task is not None:
                transaction.on_commit(self._post_process_task.si(self.pk).delay)

    def post_process(self):
        self.resize_image()

    def resize_image(self):
        original = Image.open(self.original)
        original = ImageOps.exif_transpose(original)

        for image_name, image_size in self._image_config.items():
            resized_image = ImageOps.contain(
                original, image_size, Image.Resampling.BICUBIC
            )
            django_image = pil_to_django_image(resized_image, image_name)
            setattr(self, image_name, django_image)

        self.save()
