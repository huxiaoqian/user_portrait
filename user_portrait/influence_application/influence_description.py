# -*- coding:utf-8 -*-

from elasticsearch import Elasticsearch

es = Elasticsearch("219.224.135.93")

def search_influence_detail(uid, index_name, doctype):
    result = es.get(index=index_name, doc_type=doctype, id=uid)

    return result['_source']

def influence_description(inf):
    total_list = ['origin_weibo_retweeted_total_number','origin_weibo_comment_total_number','retweeted_weibo_retweeted_total_number','retweeted_weibo_comment_total_number']
    total_threshould = [1000, 1000, 1000, 1000]
    brust_list = ['origin_weibo_retweeted_brust_average','origin_weibo_comment_brust_average','retweeted_weibo_retweeted_brust_average','retweeted_weibo_comment_brust_average']
    brust_threshould = [100, 100,100, 100]

    if inf['user_index'] < 500:
        description = "该用户影响力较低"
    elif inf['user_index'] >= 500 and inf['user_index'] <=700:
        description = "该用户影响力一般"
    elif inf['user_index'] > 700 and inf['user_index'] <=900:
        description = "该用户影响力较高"
    elif inf['user_index'] > 900 and inf['user_index'] <=1100:
        description = "该用户影响力高"
    else:
        description = "该用户影响力极高"

    if inf[total_list[0]] > total_threshould[0]:
        description = description + ',原创微博被转发量高，属于热门信息发布者'
        if inf[brust_list[0]] > brust_threshould[0]:
            description = description + ',传播速度快'
    if inf[total_list[1]] > total_threshould[1]:
        description = description + ',原创微博被评论量高，发布的热门信息容易引发公众热议'
        if inf[brust_list[1]] > brust_threshould[1]:
            description = description + ',评论速度快'
    if inf[total_list[2]] > total_threshould[2]:
        description = description + ',转发微博被转发量高，属于热门信息传播者'
        if inf[brust_list[2]] > brust_threshould[2]:
            description = description + ',传播速度快'
    if inf[total_list[3]] > total_threshould[3]:
        description = description + ',转发微博被评论量高，属于事件参与者，容易引发公众热议'
        if inf[brust_list[3]] > brust_threshould[3]:
            description = description + ',评论速度快'


    return description


if __name__ == "__main__":
    test = search_influence_detail('2693824061', '20130907', 'bci')
    print influence_description(test)


