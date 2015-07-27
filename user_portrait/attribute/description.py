# -*- coding: utf-8 -*-

def active_geo_description(result):
    active_city = {}
    active_ip = {}

    for city,value in result.items():
        count = 0
        for ip, ip_value in value.items():
            count += ip_value
            active_ip[ip] = ip_value
        active_city[city] = count

    city_count = len(active_city)
    ip_count = len(active_ip)

    active_city = sorted(active_city.iteritems(), key=lambda asd:asd[1], reverse=True)
    city = active_city[0][0]

    if city_count == 1 and ip_count <= 4:
        description = '%s为该用户的长居地，且较为固定在同一个地方登陆微博'  % city
    elif city_count >1 and ip_count <= 4:
        description = '%s多为该用户的长居地，且经常出差，较为固定在某几个地方登陆微博' % city
    elif city_count == 1 and ip_count > 4:
        description = '%s为该用户的长居地，且经常在该城市不同的地方登陆微博' % city
    else:
        description = '%s多为该用户的长居地，且经常出差，在不同的地方登陆微博' % city

    return description


def active_time_description(result):
    count = 0
    for v in result.values():
        count += v
    average = count / 6.0
    active_time_order = sorted(result.iteritems(), key=lambda asd:asd[1], reverse=True)
    active_time = {'0':'0-4', '14400':'4-8','28800':'8-12','43200':'12-16','57600':'16-20','72000':'20-24'}
    v_list = []
    for k,v in result.items():
        if v > average:
            v_list.append(active_time[k])
    definition = ','.join(v_list)
    timestamp = active_time_order[0][0]
    segment = str(int(timestamp)/4/3600)

    pd = {'0':'夜猫子','1':'早起刷微博','2':'工作时间刷微博','3':'午休时间刷微博','4':'上班时间刷微博','5':'下班途中刷微博','6':'晚间休息刷微博'}
 
    description = '用户属于%s类型，活跃时间主要集中在%s' % (pd[segment], definition)

    return description


def hashtag_description(result):
    order_hashtag = sorted(result.iteritems(), key=lambda asd:asd[1], reverse=True)
    count_hashtag = len(result)

    count = 0 
    if result:
        for v in result.values():
            count += v
        average = count / len(result)

        v_list = []
        like = order_hashtag[0][0]
        for k,v in result.items():
            if v >= average:
                v_list.append(k)
        definition = ','.join(v_list)

    if count_hashtag == 0:
        description = '该用户不喜欢参与话题讨论，讨论数为0'
    elif count_hashtag >3:
        description = '该用户热衷于参与话题讨论,热衷的话题是%s' % definition
    else:
        description = '该用户不太热衷于参与话题讨论, 参与的话题是%s' % definition

    return description

if __name__ == "__main__":
    c = {'beijing':{'219.224.135.1': 5}}
    b = {'0':2, "14400":1,"28800":3, "43200":5, "57600":2, "72000":3}
    a = {'花千骨':4}
    k = active_time_description(b)
    m = active_geo_description(c)
    n = hashtag_description(a)
    print m
    print k
    print n
