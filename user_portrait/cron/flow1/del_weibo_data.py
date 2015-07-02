# -*- coding = utf-8 -*-

import time
import os
from config import BIN_FILE_PATH

localtime = 1432396800

count = 0
file_list = os.listdir('../weibo')
for each in file_list:
    file_name = each.split('.')[0]
    file_timestamp = int(file_name.split('_')[0])
    if file_timestamp < localtime:
	os.remove('../weibo'+'/'+each)    
	count += 1
print 'we delete %s file at the time %s' %(count, localtime)
