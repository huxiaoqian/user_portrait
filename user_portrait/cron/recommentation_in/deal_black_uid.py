# -*- coding: UTF-8 -*-
'''
produce black_list from
e_business.txt  entertain.txt entertainment.txt fashion.txt sports.txt uid.txt(dzs)
'''
import csv

def get_black_uid(file_list, file_path):
    results = set()
    for file_name in file_list:
        f = open(file_path+'/'+file_name, 'rb')
        for line in f:
            uid_list = line.split(',')
            for uid in uid_list:
                uid = uid.split('\r')[0]
                uid = uid.split('\n')[0]
                results.add(uid)
        f.close()
    return results

def save_results(results):
    csvfile = open('/home/ubuntu8/huxiaoqian/user_portrait/user_portrait/cron/recommentation_in/blacklist.csv', 'wb')
    writer = csv.writer(csvfile)
    for uid in results:
        writer.writerow([uid])
    csvfile.close()

if __name__=='__main__':
    file_path = '/home/ubuntu8/yuankun/blacklist/'
    file_list = ['filter.txt', 'uid.txt', 'sports.txt', 'fashion.txt', 'entertainment.txt' ,\
                    'entertainment.txt', 'entertain.txt']
    results = get_black_uid(file_list, file_path)
    #print 'results:', results
    save_results(results)
