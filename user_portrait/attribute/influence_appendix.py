# -*- coding:utf-8 -*-
import math

def aggregation(item_list, item_dict):
    for item in item_list:
        try:
            item_dict[item] += 1
        except:
            item_dict[item] = 1
    return item_dict


def proportion(item_dict):
    results = dict()
    total = sum(item_dict.values())
    for k,v in item_dict.iteritems():
        results[k] = v/(total*1.0)
    return results

def filter_mid(mid_dict): # weibo retweeted detail or comment detail
    mid_list = []
    for k,v in mid_dict.iteritems():
        if int(v) > 0:
            mid_list.append(k)
    return mid_list


def level(item_list): # mean and standard deviation
    mean = 0
    std_var = 0
    if len(item_list):
        n = len(item_list)
        total = sum(item_list)
        mean = total/(n*1.0)
        squre_list = [item**2 for item in item_list]
        std_var = math.sqrt(sum(squre_list)/(n*1.0) - mean**2)

    result = [mean, std_var]
    return result



if __name__ == "__main__":
    print proportion({"a": 34, "v": 56, "c":77})
    print level([])
