# -*- coding:utf-8 -*-

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



if __name__ == "__main__":
    print proportion({"a": 34, "v": 56, "c":77})

