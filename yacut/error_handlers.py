from http import HTTPStatus

from flask import jsonify, render_template

from . import app, db


class InvalidAPIUsage(Exception):
    """Класс для обработки ошибок API с кодом состояния."""

    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, message, status_code=None):
        """Инициализация ошибки с сообщением и опциональным статус-кодом."""
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code

    def to_dict(self):
        """Преобразует ошибку в словарь для JSON-ответа."""
        return dict(message=self.message)


@app.errorhandler(InvalidAPIUsage)
def handle_invalid_api_usage(error):
    """Обработчик исключений InvalidAPIUsage, возвращает JSON с ошибкой."""
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.errorhandler(HTTPStatus.NOT_FOUND)
def page_not_found(error):
    """Обработчик ошибки 404, возвращает страницу 404."""
    return render_template("404.html"), HTTPStatus.NOT_FOUND


@app.errorhandler(HTTPStatus.INTERNAL_SERVER_ERROR)
def internal_error(error):
    """Обработчик ошибки 500, откатывает сессию и возвращает страницу 500."""
    db.session.rollback()
    return render_template("500.html"), HTTPStatus.INTERNAL_SERVER_ERROR
