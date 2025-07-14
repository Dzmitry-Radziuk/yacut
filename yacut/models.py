from datetime import datetime, timezone

from flask import url_for

from yacut import db
from yacut.constants import (
    FIELD_LIST,
    MAX_LENGTH_ORIGINAL_LINK,
    MAX_LENGTH_SHORT_LINK,
)


class URLMap(db.Model):
    """Модель для хранения длинных и коротких URL с меткой времени."""

    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_LENGTH_ORIGINAL_LINK), nullable=False)
    short = db.Column(db.String(MAX_LENGTH_SHORT_LINK))
    timestamp = db.Column(
        db.DateTime, index=True, default=lambda: datetime.now(timezone.utc)
    )

    def to_dict(self):
        """Преобразует объект в словарь."""
        return dict(
            url=self.original,
            short_link=url_for(
                "redirect_view", short=self.short, _external=True
            ),
        )

    def from_dict(self, data):
        """Обновляет атрибуты объекта из словаря."""
        for field in FIELD_LIST:
            if field in data:
                setattr(self, field, data[field])
