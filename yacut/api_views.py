from http import HTTPStatus

from flask import jsonify, request

from yacut import app
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap


@app.route("/api/id/", methods=["POST"])
def create_short_link():
    """Обрабатывает POST-запрос для создания короткой ссылки."""
    data = request.get_json(silent=True)

    if not data:
        raise InvalidAPIUsage("Отсутствует тело запроса")

    original = data.get("url")
    if not original:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    custom_id = data.get("custom_id")

    url_map = URLMap.create(original=original, custom_id=custom_id)
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route("/api/id/<string:short_id>/", methods=["GET"])
def get_original_link(short_id):
    url_map = URLMap.get_or_404(short_id)
    return jsonify({"url": url_map.original}), HTTPStatus.OK
