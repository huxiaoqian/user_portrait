# -*- coding: utf-8 -*-

import os
import re
import time
import redis
import datetime
import simplejson as json
from items import WeiboItem_search, UserItem_search, FriendsItem


MONGOD_HOST = 'localhost'
MONGOD_PORT = 27017
REDIS_HOST = 'localhost'
REDIS_PORT = 6379


def resp2item_search(resp, search_type, base_weibo=None, base_user=None, keywords=None):
    items = []
    if resp is None or 'deleted' in resp or ('mid' not in resp and 'screen_name' not in resp):
        return items

    if 'mid' in resp:
        weibo = WeiboItem_search(search_type)
        for key in weibo.get_resp_iter_keys():
            if key in resp:
                weibo[key] = resp[key]
        if 'user' not in weibo:
            weibo['user'] = base_user
        try:
            weibo['timestamp'] = local2unix(weibo['created_at'])
        except:
            weibo['timestamp'] = resp['created_timestamp']

        if keywords:
            weibo['keywords'] = keywords

        if base_weibo:
            base_weibo['retweeted_status'] = weibo

        items.append(weibo)
        items.extend(resp2item_search(resp.get('user'), search_type=search_type, base_weibo=weibo))
        items.extend(resp2item_search(resp.get('retweeted_status'), search_type=search_type, base_weibo=weibo, keywords=keywords))
    else:
        user = UserItem_search(search_type)
        for key in UserItem_search.RESP_ITER_KEYS:
            if key == 'screen_name':
                user['name'] = resp[key]
            if key == 'fansNum':
                user['followers_count'] = resp[key]
            if key == 'url':
                user['url'] = 'http://weibo.com' + resp['profile_url']
            if key in resp:
                if key == 'class_type':
                    user[key] = resp['class']
                else:
                    user[key] = resp[key]

        if base_weibo:
            base_weibo['user'] = user

        items.append(user)
        items.extend(resp2item_search(resp.get('status'), search_type=search_type, base_user=user))

    return items


def resp2FriendsItem(resp, item, mode='friends'):
    if not item:
        item = FriendsItem()
    else:
        item = item

    item['id'] = int(resp['user'])
    if 'ids' in resp:
        if mode == 'friends':
            item['friends'].extend(resp['ids'])
        if mode == 'followers':
            item['followers'].extend(resp['ids'])

    return item


def datetime2str(dt):
      time_format = '%Y.%m.%d'
      return dt.strftime(time_format)




def local2unix(time_str):
    time_format = '%a %b %d %H:%M:%S +0800 %Y'
    return time.mktime(time.strptime(time_str, time_format))


def localIp():
    localIP = socket.gethostbyname(socket.gethostname())#得到本地ip
    print "local ip: %s " % localIP
    return localIP

def get_pid():
    return os.getpid()

def get_ip():
    host_ip = 'Unknown'
    names, aliases, ips = socket.gethostbyname_ex(socket.gethostname())
    for ip in ips :
        if not re.match('^192', ip) and not re.match('^172', ip):
            host_ip = ip

    return host_ip


