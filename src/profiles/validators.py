from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models.fields.files import ImageFieldFile
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.core.files.base import File
from PIL import Image


@deconstructible
class AvatarValidator:
    """
    Avatar validator. Checks the image size and file size.
    Use @deconstructible decorator for serialization during migration
    """

    def __init__(self):
        self.allowed_avatar_size = (100, 100)
        self.allowed_avatar_bytes = 1048576  # 1Mb

    def __call__(self, value: 'ImageFieldFile, InMemoryUploadedFile'):
        valid_avatar_size = self.check_avatar_size(value)
        valid_avatar_bytes = self.check_avatar_bytes(value)

        if not valid_avatar_size or not valid_avatar_bytes:
            raise ValidationError('Неправильный размер изображения')

    def check_avatar_bytes(self, value: 'ImageFieldFile, InMemoryUploadedFile'):
        if value.size > self.allowed_avatar_bytes:
            return False
        return True

    def check_avatar_size(self, value: 'ImageFieldFile, InMemoryUploadedFile'):
        image_functions = {InMemoryUploadedFile: lambda val: val.image,
                           ImageFieldFile: lambda val: image_functions[val.file.__class__](val.file),
                           File: lambda val: Image.open(val)}

        avatar_size = image_functions[value.__class__](value).size

        if avatar_size != self.allowed_avatar_size:
            return False
        return True
