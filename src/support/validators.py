from django.core.exceptions import ValidationError


def validate_size_video(video):
    """Проверка размера видео"""
    megabyte_limit = 50
    if video.size > megabyte_limit * 1024 * 1024:
        raise ValidationError(f"Максимальный размер файла {megabyte_limit}MB")
