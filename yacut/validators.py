from wtforms.validators import Regexp, ValidationError

from yacut.constants import CUSTOM_ID_VALIDATOR_REG_V
from yacut.models import URLMap

custom_id_validator = Regexp(
    CUSTOM_ID_VALIDATOR_REG_V,
    message="Только латинские буквы и цифры, максимум 16 символов",
)


def unique_custom_id(form, field):
    """Проверяет, что короткий ID уникален в базе данных."""
    if field.data and URLMap.query.filter_by(short=field.data).first():
        raise ValidationError(
            "Предложенный вариант короткой ссылки уже существует."
        )
