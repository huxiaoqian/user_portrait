# -*- coding:utf-8 -*-

import sys
import re
import json
import time
from collections import Counter
from config import load_scws, load_dict, cut_filter, re_cut


sw = load_scws()
cx_dict = set(['Ag','a','an','Ng','n','nr','ns','nt','nz','Vg','v','vd','vn','@','j'])

def freq_word(items):
    """
    统计一条文本的词频，对文本进行过滤后再分词
    input:
        items:微博字典，{"mid": 12345, "text": text}
    output:
        top_word:词和词频构成的字典，如:{词:词频, 词:词频}
    """

    word_list = []
    text = items["text"]
    text = re_cut(text)
    cut_text = sw.participle(text)
    print cut_text
    cut_word_list = [term for term, cx in cut_text if cx in cx_dict]
    for w in cut_word_list:
        word_list.append(w)

    counter = Counter(word_list)
    total = sum(counter.values())
    topk_words = counter.most_common()
    top_word = {k:(float(v)/float(total)) for k,v in topk_words}

    return top_word


def tfidf(inputs):
    """
    计算每条文本中每个词的tfidf，对每个词在各个文本中tfidf加和除以出现的文本次数作为该词的权值
    输入数据：
        inputs: [{"mid": mid, "text": text}]
    输出结果：
        result_tfidf[:topk]:前20%tfidf词及tfidf值的列表,示例：[(词,tfidf)]
        input_word_dict:每一条记录的词及tfidf,示例：{"_id":{词：tfidf,词：tfidf,...}}
    """

    total_document_count = len(inputs)
    tfidf_dict = {} #词在各个文本中的tfidf之和
    count_dict = {} #词出现的文本数
    count = 0 #记录每类下词频总数
    input_word_dict = {} #每条记录每个词的tfidf,{"_id":{词：tfidf，词：tfidf}}
    for input in inputs:
        word_count = freq_word(input)
        count += sum(word_count.values())
        word_tfidf_row = {}#每一行中词的tfidf
        for k,v in word_count.iteritems():
            tf = v
            document_count = sum([1 for input_item in inputs if k in input_item['text']])
            idf = math.log(float(total_document_count)/(float(document_count+1)))
            tfidf = tf*idf
            word_tfidf_row[k] = tfidf
            try:
                tfidf_dict[k] += tfidf
            except:
                tfidf_dict[k] = 1
        input_word_dict[input["_id"]] = word_tfidf_row

    for k,v in tfidf_dict.iteritems():
        tfidf_dict[k] =  float(tfidf_dict[k])/float(len(inputs))

    sorted_tfidf = sorted(tfidf_dict.iteritems(), key = lambda asd:asd[1],reverse = True)
    result_tfidf = [(k,v)for k,v in sorted_tfidf]

    topk = int(math.ceil(float(len(result_tfidf))*0.2))#取前20%的tfidf词
    return result_tfidf[:topk],input_word_dict


def process_for_cluto(word, inputs, version=)


if __name__ == "__main__":
    print freq_word({"mid": "12345", "text": "回复：无与伦比的美丽，转发微博啊"})
