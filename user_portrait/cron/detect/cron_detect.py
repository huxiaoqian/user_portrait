#-*- coding:utf-8 -*-
import os
import time


#use to detect group by single-person
#input: {}
#output: {}
def single_detect():
    results = {}
    #step1: identify the uid or uname is right
    #step2: get user by three type parameter
    return results

#use to detect group by multi-person
#input: {}
#output: {}
def multi_detect():
    results = {}
    return results

#use to detect group by attribute or pattern
#input: {}
#output: {}
def attribute_pattern_detect():
    results = {}
    return results

#use to detect group by event
#input: {}
#output: {}
def event_detect():
    results = {}
    return results

#use to save detect results to es
#input: {}
#output: {}
def save_detect_results(detect_results):
    mark = Flase
    return mark

#use to change detect task process proportion
def change_process_proportion(task_name, proportion):
    mark = False
    return mark


#use to get detect information from redis queue
def get_detect_information():
    results = {}
    return results

#main function to group detect
def compute_group_detect():
    results = {}
    while True:
        #step1:read detect task information from redis queue
        detect_task_information = get_detect_information()
        #step2:according task type to do group detect
        detect_task_type = detect_task_information['detect_type']
        if detect_task_type == 'single':
            detect_results = single_detect(detect_task_information)
        elif detect_task_type == 'multi':
            detect_results == multi_detect(detect_task_information)
        elif detect_task_type == 'attribute':
            detect_results =  attribute_pattern_detect(detect_task_information)
        elif detect_task_type == 'event':
            detect_results = event_detect(detect_task_information)
        mark = save_detect_results(detect_results)



if __name__=='__main__':
    compute_group_detect()
