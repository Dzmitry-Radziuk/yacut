from http import HTTPStatus
from flask import jsonify, render_template, request
from yacut import app, db


class ShortIDNotUniqueError(Exception):
    """ID уже существует."""

    status_code = HTTPStatus.CONFLICT

    def __init__(
        self, message="Предложенный вариант короткой ссылки уже существует."
    ):
        self.message = message
        super().__init__(message)


class InvalidShortIDNameError(Exception):
    """Недопустимое имя."""

    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message="Указано недопустимое имя для короткой ссылки"):
        self.message = message
        super().__init__(message)


class ShortIDNotFoundError(Exception):
    """ID не найден."""

    status_code = HTTPStatus.NOT_FOUND

    def __init__(self, message="Указанный id не найден"):
        self.message = message
        super().__init__(message)


class ShortIDAlreadyExistsError(Exception):
    """Не удалось создать ID."""

    status_code = HTTPStatus.SERVICE_UNAVAILABLE

    def __init__(
        self,
        message="Не удалось сгенерировать уникальный короткий ID"
                "за максимально допустимое число попыток",
    ):
        self.message = message
        super().__init__(message)


class InvalidAPIUsage(Exception):
    """Ошибка API."""

    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message, status_code=None):
        self.message = message
        super().__init__(message)
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        """Преобразует в словарь."""
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def handle_invalid_api_usage(error):
    """Ответ с ошибкой API."""
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(ShortIDNotUniqueError)
def handle_short_id_not_unique(error):
    """ID уже занят."""
    response = jsonify({"message": error.message})
    response.status_code = error.status_code
    return response


@app.errorhandler(InvalidShortIDNameError)
def handle_invalid_short_id_name(error):
    """Недопустимое имя."""
    response = jsonify({"message": error.message})
    response.status_code = error.status_code
    return response


@app.errorhandler(ShortIDNotFoundError)
def handle_short_id_not_found(error):
    """ID не найден, JSON или HTML."""
    if (
        request.accept_mimetypes.accept_json
        and not request.accept_mimetypes.accept_html
    ):
        response = jsonify({"message": error.message})
        response.status_code = error.status_code
        return response
    return render_template("404.html"), error.status_code


@app.errorhandler(ShortIDAlreadyExistsError)
def handle_short_id_already_exists(error):
    """Не удалось создать ID."""
    response = jsonify({"message": error.message})
    response.status_code = error.status_code
    return response


@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(error):
    """Страница 404."""
    return render_template("404.html"), HTTPStatus.NOT_FOUND


@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_error(error):
    """Страница 500."""
    db.session.rollback()
    return render_template("500.html"), HTTPStatus.INTERNAL_SERVER_ERROR
