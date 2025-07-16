from http import HTTPStatus

from flask import jsonify, request

from yacut import app, error_handlers
from yacut.models import URLMap


@app.route("/api/id/", methods=["POST"])
def create_short_link():
    """Создает короткую ссылку из JSON с 'url' и опциональным 'custom_id'."""
    data = request.get_json(silent=True)
    if not data:
        raise error_handlers.InvalidAPIUsage("Отсутствует тело запроса")

    original = data.get("url")
    if not original:
        raise error_handlers.InvalidAPIUsage(
            '"url" является обязательным полем!'
        )

    custom_id = data.get("custom_id")

    try:
        url_map = URLMap.create(original=original, custom_id=custom_id)
    except error_handlers.ShortIDNotUniqueError as error:
        raise error_handlers.InvalidAPIUsage(
            str(error), HTTPStatus.BAD_REQUEST
        )
    except error_handlers.InvalidShortIDNameError as error:
        raise error_handlers.InvalidAPIUsage(
            str(error), HTTPStatus.BAD_REQUEST
        )
    except error_handlers.ShortIDAlreadyExistsError as error:
        raise error_handlers.InvalidAPIUsage(
            str(error), HTTPStatus.BAD_REQUEST
        )
    except Exception:
        raise error_handlers.InvalidAPIUsage(
            "Внутренняя ошибка сервера", HTTPStatus.INTERNAL_SERVER_ERROR
        )

    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route("/api/id/<string:short_id>/", methods=["GET"])
def get_original_link(short_id):
    """Возвращает оригинальный URL по короткому идентификатору."""
    try:
        url_map = URLMap.get_or_404(short_id)
    except error_handlers.ShortIDNotFoundError as error:
        raise error_handlers.InvalidAPIUsage(str(error), HTTPStatus.NOT_FOUND)
    return jsonify({"url": url_map.original}), HTTPStatus.OK
