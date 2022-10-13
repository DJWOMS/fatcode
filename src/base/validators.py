from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models.fields.files import ImageFieldFile
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.core.files.base import File
from PIL import Image


@deconstructible
class ImageValidator:
    """
    Avatar and logo validator. Checks the image size and file size.
    Use @deconstructible decorator for serialization during migration
    """

    def __init__(self, img_size: tuple, img_bytes: int):
        self.img_size = img_size
        self.img_bytes = img_bytes

    def __call__(self, value: 'ImageFieldFile, InMemoryUploadedFile'):
        valid_image_size = self.check_image_size(value)
        valid_image_bytes = self.check_image_bytes(value)

        if not valid_image_size:
            raise ValidationError('Неправильный размер изображения')
        elif not valid_image_bytes:
            raise ValidationError('Неправильный вес изображения')

    def check_image_bytes(self, value: 'ImageFieldFile, InMemoryUploadedFile'):
        if value.size > self.img_bytes:
            return False
        return True

    def check_image_size(self, value: 'ImageFieldFile, InMemoryUploadedFile'):
        image_functions = {
            InMemoryUploadedFile: lambda val: val.image,
            ImageFieldFile: lambda val: image_functions[val.file.__class__](val.file),
            File: lambda val: Image.open(val)
        }

        image_size = image_functions[value.__class__](value).size

        if image_size > self.img_size:
            return False
        return True
