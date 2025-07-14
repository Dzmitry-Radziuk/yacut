from http import HTTPStatus

from flask import abort, flash, redirect, render_template

from yacut import app, db
from yacut.forms import URLForm
from yacut.models import URLMap
from yacut.utils import get_unique_short_id


@app.route("/<short>")
def redirect_view(short):
    """Перенаправляет на оригинальный URL по короткому идентификатору."""
    url_map_object = URLMap.query.filter_by(short=short).first()
    if url_map_object:
        return redirect(url_map_object.original)
    else:
        abort(HTTPStatus.NOT_FOUND)


@app.route("/", methods=["GET", "POST"])
def index_view():
    """Обрабатывает главную страницу и создание коротких ссылок."""
    form = URLForm()
    if form.validate_on_submit():
        custom_id = form.custom_id.data or get_unique_short_id()
        original_link = form.original_link.data
        url_map_object = URLMap(original=original_link, short=custom_id)
        db.session.add(url_map_object)
        db.session.commit()
        flash("Ссылка успешно создана!", "success")
        return render_template(
            "index.html", form=form, url_map_object=url_map_object
        )
    return render_template("index.html", form=form)
