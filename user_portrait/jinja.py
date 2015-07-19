# -*- coding: utf-8 -*-

from datetime import date


def gender(g):
	if g == 1:
		return u'/../../static/img/male.png'
	elif g == 2:
		return u'/../../static/img/female.png'
	else:
		return u''

def gender_text(g):
	if g == 1:
		return u'男'
	elif g == 2:
		return u'女'
	else:
		return u'未知'

def Int2string(g):
	return str(g) 


def tsfmt(ts):
    return date.fromtimestamp(ts) if ts else None
