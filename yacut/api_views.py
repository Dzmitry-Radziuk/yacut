from http import HTTPStatus

from flask import jsonify, request

from yacut import app, db
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap
from yacut.utils import get_unique_short_id
from yacut.validators import custom_id_validator


@app.route("/api/id/", methods=["POST"])
def create_short_link():
    """Обрабатывает POST-запрос для создания короткой ссылки."""
    data = request.get_json(silent=True)
    if not data:
        raise InvalidAPIUsage("Отсутствует тело запроса")

    url_field = data.get("url")
    if url_field is None:
        raise InvalidAPIUsage('"url" является обязательным полем!')

    short_link = data.get("custom_id")

    if short_link:
        if URLMap.query.filter_by(short=short_link).first() is not None:
            raise InvalidAPIUsage(
                "Предложенный вариант короткой ссылки уже существует."
            )
        if custom_id_validator.regex.match(short_link) is None:
            raise InvalidAPIUsage(
                "Указано недопустимое имя для короткой ссылки"
            )
    else:
        short_link = get_unique_short_id()
    url_map = URLMap(original=url_field, short=short_link)
    db.session.add(url_map)
    db.session.commit()
    return jsonify(url_map.to_dict()), HTTPStatus.CREATED


@app.route("/api/id/<string:short_id>/", methods=["GET"])
def get_original_link(short_id):
    """Возвращает оригинальную ссылку по короткому идентификатору."""
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is not None:
        return jsonify({"url": url_map.original}), HTTPStatus.OK
    raise InvalidAPIUsage("Указанный id не найден", HTTPStatus.NOT_FOUND)
