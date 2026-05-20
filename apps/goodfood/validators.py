from string import ascii_letters, digits

import magic
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class GoodfoodValidator:
    ALLOWED_CHARACTERS = (
        ascii_letters
        + digits
        + "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯ"
        + "абвгдеёжзийклмнопрстуфхцчшщьыъэюя"
        + " -,.;:!?"
    )

    def __init__(self, message=None):
        self.message = (
            message if message else "input should be Ascii_letters, Digits or Cyrillic"
        )

    def __call__(self, value):
        if value is None:
            return

        value = str(value)
        if not (set(value) <= set(self.ALLOWED_CHARACTERS)):
            raise ValidationError(self.message, params={"value": value})


def validate_image_file(file):
    allowed_types = ["image/jpeg", "image/png", "image/webp"]
    mime = magic.from_buffer(file.read(1024), mime=True)
    file.seek(0)
    if mime not in allowed_types:
        raise ValidationError(f"Недопустимый тип файла: {mime}")
