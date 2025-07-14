from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Optional

from yacut.validators import custom_id_validator, unique_custom_id


class URLForm(FlaskForm):
    """Форма для создания короткой ссылки с валидацией полей."""

    original_link = URLField(
        "Оригинальная ссылка",
        validators=[
            DataRequired("Поле обязательно для заполнения"),
            URL("Введите корректный URL"),
        ],
    )
    custom_id = StringField(
        "Ваш вариант короткой ссылки",
        validators=[
            Optional(),
            custom_id_validator,
            unique_custom_id,
        ],
    )
    submit = SubmitField("Создать")
