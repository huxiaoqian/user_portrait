# -*- coding: utf-8 -*-

from flask import views, Blueprint, render_template

from user_portrait.extensions import es_get_source, es_mget_source

bp = Blueprint('user', __name__, url_prefix='/user')


class UserView(views.MethodView):
    """
    单个用户的个人信息页面
    """
    template = 'individual.html'

    def get(self, id):
        user = es_get_source(id)
        followers = []
        friends = []
        if user:
            user_followers_ids = user.get('followers')
            user_friends_ids = user.get('friends')
            if user_followers_ids:
                followers = es_mget_source(user_followers_ids)
            if user_friends_ids:
                friends = es_mget_source(user_friends_ids)

        return render_template(self.template, user=user,
                               followers=followers, friends=friends,
                               id=id)


class UserFollowersView(views.MethodView):
    """
    单个用户与粉丝的关联延伸
    """

    template = 'individual_followers.html'

    def get(self, id):
        return render_template(self.template, id=id)


class UserFriendsView(views.MethodView):
    """
    单个用户与好友的关联延伸
    """

    template = 'individual_friends.html'

    def get(self, id):
        return render_template(self.template, id=id)


bp.add_url_rule('/<id>/', view_func=UserView.as_view('detail'))
bp.add_url_rule('/<id>/followers/', view_func=UserFollowersView.as_view('followers'))
bp.add_url_rule('/<id>/friends/', view_func=UserFriendsView.as_view('friends'))
