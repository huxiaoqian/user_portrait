#-*- coding:utf-8 -*-

import os
import json
from flask import Blueprint, url_for, render_template, request, abort, flash, session, redirect

mod = Blueprint('attribtue', __name__, url_prefix='/attribute')

@mod.route('/ip/')
def ajax_ip():
    mtype = request.args.get('style', '')
    mtype = int(mtype)
    
    return json.dumps(results)

@mod.route('//')

