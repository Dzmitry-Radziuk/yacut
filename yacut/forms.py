from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional

from yacut.constants import (
    MAX_LENGTH_ORIGINAL_LINK,
    MAX_LENGTH_SHORT_LINK,
    ONE,
)
from yacut.validators import custom_id_validator


class URLForm(FlaskForm):
    """Форма для создания короткой ссылки с валидацией полей."""

    original_link = URLField(
        "Оригинальная ссылка",
        validators=[
            DataRequired("Поле обязательно для заполнения"),
            URL("Введите корректный URL"),
            Length(ONE, MAX_LENGTH_ORIGINAL_LINK),
        ],
    )
    custom_id = StringField(
        "Ваш вариант короткой ссылки",
        validators=[
            Optional(),
            custom_id_validator,
            Length(ONE, MAX_LENGTH_SHORT_LINK),
        ],
    )
    submit = SubmitField("Создать")
