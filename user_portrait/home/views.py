# -*- coding:utf-8 -*-

from flask import views, Blueprint, render_template

mod = Blueprint('home',__name__)

class HomeView(views.MethodView):
    templates = 'portrait/tag.html'

    def get(self):
        return render_template(self.templates)
mod.add_url_rule('/', view_func=HomeView.as_view('index'))
