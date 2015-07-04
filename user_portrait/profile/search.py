# -*- coding: utf-8 -*-

from flask import views, Blueprint, render_template

from user_portrait.extensions import es

from .form import SearchForm

bp = Blueprint('search', __name__, url_prefix='/search')


class SearchView(views.MethodView):
    """多维度复杂检索页"""

    template = ''

    def get(self):
        form = SearchForm()
        return render_template(self.template, form=form)

    def post(self):
        form = SearchForm()
        if not form.validate_on_submit():
            return render_template(self.template, form=form)
        # TODO es search
        try:
            source = es.search(size=100)
        except Exception as e:
            raise e
        return render_template(self.template, source=source)


bp.add_url_rule('/', view_func=SearchView.as_view('index'))
