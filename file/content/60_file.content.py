#!/usr/bin/python
#coding:utf-8
# author: wangkai
# date: 2015-06-13
# 返回值说明：0 - 正常，-1 - 检查脚本异常, 1 - 文件内容发生改变
# 如果产生diff的文件内容，则始终输出1，直到diff文件被清理，清理文件:/tmp/.falcon.<filename path>.diff*
# 如果被检查的文件被多次改变，则产生多个带timestamp的diff文件

import os
import sys
import time
import json
import socket
import shutil
import difflib
import requests

#####该部分用于配置被检查文件、临时文件、diff文件######
file_list = [
    '/etc/passwd',
    '/etc/shadow'
]

file_dict = {}
for fname in file_list:
    file_dict[fname] = {}
    file_dict[fname]['ftmp'] = '/tmp/.falcon' + '.'.join(fname.split('/')) + '.tmp'
    file_dict[fname]['fdiff'] = '/tmp/.falcon' + '.'.join(fname.split('/')) + '.diff'

timestamp = str(int(time.time()))
result = []
#######################################################

#####该部分定义push的接口，metric名称，tags等信息######
falcon_api = 'http://127.0.0.1:2015/v1/push'
endpoint = socket.gethostname()
metric = 'file.content'
step = 60
counterType = "GAUGE"
#######################################################

def push_data(fname, value):
    ts = int(timestamp)
    payload = {
        "endpoint": endpoint,
	"metric": metric,
	"timestamp": ts,
	"step": step,
	"value": value,
	"counterType": counterType,
	"tags": 'filename=' + fname
    }
    result.append(payload)
    #r = requests.post(falcon_api, data=json.dumps(payload))
    #print r.text

def check_file(fname, ftmp, fdiff):
    try:
        if os.path.isfile(ftmp):
            f1 = open(fname).readlines()
    	    f2 = open(ftmp).readlines()
    	    diff = ''.join(difflib.context_diff(f1, f2, fromfile='原内容', tofile='变化后的内容'))
    	    if os.path.isfile(fdiff):
                if diff:
    		    open(fdiff+'-'+timestamp, 'w').write(diff)
                    shutil.copy2(fname, ftmp)
                push_data(fname, 1)
    	    else:
    	        if diff:
    		    open(fdiff, 'w').write(diff)
                    shutil.copy2(fname, ftmp)
    		    push_data(fname, 1)
    	        else:
    	            push_data(fname, 0)
        else:
    	    shutil.copy2(fname, ftmp)
    	    push_data(fname, 0)
    except Exception, e:
	push_data(fname, -1)

def main():
    for k in file_dict.keys():
	check_file(k, file_dict[k]['ftmp'], file_dict[k]['fdiff'])
   
if __name__ == "__main__":
    main()
    print json.dumps(result)
