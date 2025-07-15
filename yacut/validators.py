from wtforms.validators import Regexp

from yacut.constants import CUSTOM_ID_VALIDATOR_REG_V

custom_id_validator = Regexp(
    CUSTOM_ID_VALIDATOR_REG_V,
    message="Только латинские буквы и цифры, максимум 16 символов",
)
