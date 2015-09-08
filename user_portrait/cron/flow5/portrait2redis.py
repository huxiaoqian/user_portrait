# -*- coding=utf-8 -*-
'''
this is a task which to be started in 23:00 every day
use to read uid list who is in es_user_portrait
'''
import sys
from elasticsearch.helpers import scan
reload(sys)
sys.path.append('../../')

from time_utils import ts2datetime, datetime2ts
from global_utils import es_user_portrait as es

# mark es_user_portrait: index, doc_type
user_portrait_index = 'user_portrait'
user_portrait_type = 'user'

# use to write uid from user_portrait to RAM
# scan es
def read_portrait2ram():
    index_exist = es.indices.exists(index=user_portrait_index)
    if not index_exist:
        print 'no user_portrait'
    else:
        s_re = scan(es, query={'query':{'match_all':{}}, 'size':1000}, \
                    index=user_portrait_index, doc_type=user_portrait_type)
        user_list = []
        count = 0
        while True:
            try:
                scan_re = s_re.next()['_source']
                count += 1
                user_list.append(scan_re['uid'])
            except StopIteration:
                print 'all done'
                break
            except Exception, e:
                print Exception, e
                sys.exit(0)
    '''
    print count
    print 'len uid_list:', len(user_list)
    print 'one uid:', user_list[0], len(user_list[0]), type(user_list[0])
    '''
    return user_list

if __name__=='__main__':
    read_portrait2ram()
