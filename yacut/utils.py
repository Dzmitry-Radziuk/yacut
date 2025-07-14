import random
import string

from yacut.constants import DEFAULT_LENGTH_SHORT_LINK
from yacut.models import URLMap


def get_unique_short_id(length=DEFAULT_LENGTH_SHORT_LINK):
    """Генерирует уникальный короткий идентификатор заданной длины."""
    characters = string.ascii_letters + string.digits
    while True:
        short = "".join(random.choices(characters, k=length))
        if not URLMap.query.filter_by(short=short).first():
            return short
