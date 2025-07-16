import random
import string
from datetime import datetime, timezone

from flask import url_for

from yacut import db, error_handlers
from yacut.constants import (
    DEFAULT_LENGTH_SHORT_LINK,
    MAX_GENERATE_ATTEMPTS,
    MAX_LENGTH_ORIGINAL_LINK,
    MAX_LENGTH_SHORT_LINK,
    ORIGINAL_FIELD,
    SHORT_FIELD,
)
from yacut.validators import custom_id_validator


class URLMap(db.Model):
    """Модель хранения пар 'длинная ссылка – короткий ID'."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LENGTH_ORIGINAL_LINK), nullable=False)
    short = db.Column(db.String(MAX_LENGTH_SHORT_LINK))
    timestamp = db.Column(
        db.DateTime, index=True, default=lambda: datetime.now(timezone.utc)
    )

    def get_short_url(self):
        """Возвращает абсолютный URL по short ID."""
        return url_for("redirect_view", short=self.short, _external=True)

    def to_dict(self):
        """Преобразует объект в словарь для JSON-ответа."""
        return {
            "url": self.original,
            "short_link": self.get_short_url(),
        }

    def from_dict(self, data):
        """Заполняет поля модели из словаря."""
        if ORIGINAL_FIELD in data:
            self.original = data[ORIGINAL_FIELD]
        if SHORT_FIELD in data:
            self.short = data[SHORT_FIELD]

    @staticmethod
    def generate_unique_short_id(length=DEFAULT_LENGTH_SHORT_LINK):
        """Генерирует уникальный short ID."""
        characters = string.ascii_letters + string.digits
        for _ in range(MAX_GENERATE_ATTEMPTS):
            short = "".join(random.choices(characters, k=length))
            if not URLMap.get_by_short_id(short):
                return short
        raise error_handlers.ShortIDAlreadyExistsError()

    @staticmethod
    def get_by_short_id(short_id):
        """Возвращает объект по short ID или None."""
        return URLMap.query.filter_by(short=short_id).first()

    @staticmethod
    def ensure_short_id_is_unique(short_id):
        """Проверяет, что short ID уникален."""
        if short_id and URLMap.get_by_short_id(short_id):
            raise error_handlers.ShortIDNotUniqueError()

    @staticmethod
    def create(original, custom_id=None):
        """Создаёт и сохраняет новую запись."""
        if custom_id:
            URLMap.ensure_short_id_is_unique(custom_id)
            if not custom_id_validator.regex.match(custom_id):
                raise error_handlers.InvalidShortIDNameError()
            short = custom_id
        else:
            short = URLMap.generate_unique_short_id()

        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @staticmethod
    def get_or_404(short_id):
        """Возвращает объект по short ID или кидает ошибку."""
        url_map = URLMap.get_by_short_id(short_id)
        if not url_map:
            raise error_handlers.ShortIDNotFoundError()
        return url_map

    def __repr__(self):
        """Возвращает строковое представление объекта."""
        return f"<URLMap short={self.short} original={self.original}>"
