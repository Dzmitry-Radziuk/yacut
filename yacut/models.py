import random
import string
from datetime import datetime, timezone
from http import HTTPStatus

from flask import url_for

from yacut import db
from yacut.constants import (
    DEFAULT_LENGTH_SHORT_LINK,
    MAX_GENERATE_ATTEMPTS,
    MAX_LENGTH_ORIGINAL_LINK,
    MAX_LENGTH_SHORT_LINK,
    ORIGINAL_FIELD,
    SHORT_FIELD,
)
from yacut.error_handlers import InvalidAPIUsage
from yacut.validators import custom_id_validator


class URLMap(db.Model):
    """Модель для хранения длинных и коротких URL с меткой времени."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LENGTH_ORIGINAL_LINK), nullable=False)
    short = db.Column(db.String(MAX_LENGTH_SHORT_LINK))
    timestamp = db.Column(
        db.DateTime, index=True, default=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self):
        """Возвращает объект в виде словаря."""
        return {
            "url": self.original,
            "short_link": url_for(
                "redirect_view", short=self.short, _external=True
            ),
        }

    def from_dict(self, data):
        """Обновляет поля из словаря."""
        if ORIGINAL_FIELD in data:
            self.original = data[ORIGINAL_FIELD]
        if SHORT_FIELD in data:
            self.short = data[SHORT_FIELD]

    @staticmethod
    def generate_unique_short_id(length=DEFAULT_LENGTH_SHORT_LINK):
        characters = string.ascii_letters + string.digits
        for _ in range(MAX_GENERATE_ATTEMPTS):
            short = "".join(random.choices(characters, k=length))
            if not URLMap.get_by_short_id(short):
                return short
        raise RuntimeError(
            "Не удалось сгенерировать уникальный короткий ID"
            "за максимально допустимое число попыток"
        )

    @staticmethod
    def get_by_short_id(short_id):
        """Возвращает объект по короткому ID или None."""
        return URLMap.query.filter_by(short=short_id).first()

    @staticmethod
    def ensure_short_id_is_unique(short_id):
        """Проверяет уникальность short_id или бросает исключение."""
        if short_id and URLMap.get_by_short_id(short_id):
            raise InvalidAPIUsage(
                "Предложенный вариант короткой ссылки уже существует."
            )

    @staticmethod
    def create(original, custom_id=None):
        """Создаёт и сохраняет новую короткую ссылку."""
        if custom_id:
            URLMap.ensure_short_id_is_unique(custom_id)
            if not custom_id_validator.regex.match(custom_id):
                raise InvalidAPIUsage(
                    "Указано недопустимое имя для короткой ссылки"
                )
            short = custom_id
        else:
            short = URLMap.generate_unique_short_id()

        url_map = URLMap(original=original, short=short)
        db.session.add(url_map)
        db.session.commit()
        return url_map

    @staticmethod
    def get_or_404(short_id):
        """Возвращает объект по короткому ID или бросает исключение 404."""
        url_map = URLMap.get_by_short_id(short_id)
        if not url_map:
            raise InvalidAPIUsage(
                "Указанный id не найден", HTTPStatus.NOT_FOUND
            )
        return url_map

    def __repr__(self):
        return f"<URLMap short={self.short} original={self.original}>"
