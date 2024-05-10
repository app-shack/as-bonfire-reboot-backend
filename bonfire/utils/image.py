import io

import requests
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image


def generate_test_image(size=(50, 50), color=(155, 0, 0), name="test.jpg"):
    file = io.BytesIO()
    image = Image.new("RGB", size=size, color=color)
    image.save(file, "JPEG")
    file.name = name
    file.seek(0)
    return file


def pil_to_django_image(image: Image.Image, name: str):
    buffer = io.BytesIO()
    image.convert("RGBA").save(fp=buffer, format="PNG", optimize=True)
    django_file = ContentFile(buffer.getvalue())
    buffer.close()
    return InMemoryUploadedFile(
        django_file, None, f"{name}.png", "image/png", django_file.tell, None
    )


def url_to_django_image(url: str, name: str):
    binary_image = requests.get(url).content
    image = Image.open(io.BytesIO(binary_image))
    return pil_to_django_image(image, name)
