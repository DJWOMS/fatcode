import uuid


def cat_directory_path(instance, filename: str) -> str:
    """Сгенерировать путь к файлу кота при загрузке"""
    return f'cat/avatar/user_{instance.id}/{str(uuid.uuid4())}.{filename.split(".")[-1]}'


def product_directory_path(instance, filename: str) -> str:
    """Сгенерировать путь к файлу продукта при загрузке"""
    return f'product/image/product_{instance.id}/{str(uuid.uuid4())}.{filename.split(".")[-1]}'
