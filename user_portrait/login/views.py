 #-*- coding:utf-8 -*-

import os
import time

from flask import Flask, Blueprint, url_for, render_template, request,  session, redirect, escape
# temporary use
from user_portrait.global_utils import R_ADMIN as r
mod = Blueprint('login', __name__, url_prefix='/login')


@mod.route('/welcome')
def index():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return render_template('LoginManage.html')


@mod.route('/login/')
def login():
    username = request.args.get('username','')
    password = request.args.get('password','')

    if not username or not password:
        return "please enter username or password"

    admin = r.hgetall('admin')
    keys = admin.keys()
    if username in set(keys):
        vertify_passwd = admin[username]
        if password == vertify_passwd:
            vertify_result = True
        else:
            return "password is not correct"
    else:
        return "username is not correct"

    if vertify_result:
        session['username'] = username
        return 'true'
        #return redirect('/index/');


@mod.route('/logout/') # log out
def logout():
    session.pop('username', None)
    return redirect(url_for('.index'))

@mod.route('/revise_password') # revise password
def revise_password():
    username = request.args.get('username','')
    old_password = request.args.get('old_password','')
    new_password = request.args.get('new_password','')

    if not username or not old_password or not new_password:
        return "please complete enter"

    admin = r.hgetall('admin')
    keys = admin.keys()
    if username in set(keys):
        vertify_passwd = admin[username]
        if old_password == vertify_passwd:
            vertify_result = True
            r.hset('admin', username, new_password)
            return "revise complete"
        else:
            return "password is not correct"
    else:
        return "username is not correct"


