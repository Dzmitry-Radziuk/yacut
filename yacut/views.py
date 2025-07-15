from flask import flash, redirect, render_template

from yacut import app
from yacut.error_handlers import InvalidAPIUsage
from yacut.forms import URLForm
from yacut.models import URLMap


@app.route("/<short>")
def redirect_view(short):
    """Перенаправляет на оригинальный URL по короткому идентификатору."""
    url_map_object = URLMap.get_or_404(short)
    return redirect(url_map_object.original)


@app.route("/", methods=["GET", "POST"])
def index_view():
    """Обрабатывает форму создания короткой ссылки и отображает результат."""
    form = URLForm()
    url_map_object = None

    if form.validate_on_submit():
        original_link = form.original_link.data
        custom_id = form.custom_id.data

        try:
            url_map_object = URLMap.create(
                original=original_link, custom_id=custom_id
            )
            flash("Ссылка успешно создана")
        except InvalidAPIUsage as error:
            form.custom_id.errors.append(error.message)

    return render_template(
        "index.html", form=form, url_map_object=url_map_object
    )