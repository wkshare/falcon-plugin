#!/usr/bin/python
#coding:utf8
# author: wangkai
# date: 2015-06-24

import json
import time
import socket
import psutil

#需要检查的进程列表
process_list = [
    "ntpd",
    "cron",
    "rsyslogd",
    "mysqld"
]

#####该部分定义push的接口，metric名称，tags等信息######
falcon_api = 'http://127.0.0.1:2015/v1/push'
endpoint = socket.gethostname()
timestamp = int(time.time())
process_result = []
#######################################################

def main():
    for proc in psutil.process_iter():
        if proc.name in process_list:
            tags = 'process_name=%s' % proc.name
            #进程的状态
            process_status = proc.status
            if process_status == psutil.STATUS_RUNNING:
                process_status = 0
            elif process_status == psutil.STATUS_SLEEPING:
                process_status = 1
            elif process_status == psutil.STATUS_IDLE:
                process_status = 2
            elif process_status == psutil.STATUS_WAKING:
                process_status = 3
            elif process_status == psutil.STATUS_LOCKED:
                process_status = 4
            elif process_status == psutil.STATUS_TRACING_STOP:
                process_status = 5
            elif process_status == psutil.STATUS_STOPPED:
                process_status = 6
            elif process_status == psutil.STATUS_DISK_SLEEP:
                process_status = -1
            elif process_status == psutil.STATUS_DEAD:
                process_status = -2
            elif process_status == psutil.STATUS_ZOMBIE:
                process_status = -3
            else:
                process_status = 1
            member = {
                "metric": "process_status",
                "endpoint": endpoint,
                "timestamp": timestamp,
                "step": 60,
                "value": process_status,
                "counterType": "GAUGE",
                "tags": tags
            }
            process_result.append(member)

            #进程的网络连接数，暂时不拆分更详细的联系状态
            process_connections = len(proc.get_connections())
            member = {
                "metric": "process_connections",
                "endpoint": endpoint,
                "timestamp": timestamp,
                "step": 60,
                "value": process_connections,
                "counterType": "GAUGE",
                "tags": tags
            }
            process_result.append(member)
            #cpu的使用率
            process_cpu_percent = proc.get_cpu_percent()
            member = {
                "metric": "process_cpu_percent",
                "endpoint": endpoint,
                "timestamp": timestamp,
                "step": 60,
                "value": process_cpu_percent,
                "counterType": "GAUGE",
                "tags": tags
            }
            process_result.append(member)

            #物理内存和虚拟内存的使用，内存使用占比
            memory_info = proc.get_memory_info()
            process_mem_rss = memory_info[0]
            member = {
                "metric": "process_mem_rss",
                "endpoint": endpoint,
                "timestamp": timestamp,
                "step": 60,
                "value": process_mem_rss,
                "counterType": "GAUGE",
                "tags": tags
            }
            process_result.append(member)
            process_mem_vms = memory_info[1]
            member = {
                "metric": "process_mem_vms",
                "endpoint": endpoint,
                "timestamp": timestamp,
                "step": 60,
                "value": process_mem_vms,
                "counterType": "GAUGE",
                "tags": tags
            }
            process_result.append(member)
            process_mem_percent = round(proc.get_memory_percent(),3)
            member = {
                "metric": "process_mem_percent",
                "endpoint": endpoint,
                "timestamp": timestamp,
                "step": 60,
                "value": process_mem_percent,
                "counterType": "GAUGE",
                "tags": tags
            }
            process_result.append(member)

            #open file的数量
            process_open_files = len(proc.get_open_files())
            member = {
                "metric": "process_open_files",
                "endpoint": endpoint,
                "timestamp": timestamp,
                "step": 60,
                "value": process_open_files,
                "counterType": "GAUGE",
                "tags": tags
            }
            process_result.append(member)

            #进程的线程数量
            process_num_threads = proc.get_num_threads()
            member = {
                "metric": "process_num_threads",
                "endpoint": endpoint,
                "timestamp": timestamp,
                "step": 60,
                "value": process_num_threads,
                "counterType": "GAUGE",
                "tags": tags
            }
            process_result.append(member)

            #进程io相关数据
            io_counters = proc.get_io_counters()
            process_read_count = io_counters[0]
            member = {
                "metric": "process_read_count",
                "endpoint": endpoint,
                "timestamp": timestamp,
                "step": 60,
                "value": process_read_count,
                "counterType": "COUNTER",
                "tags": tags
            }
            process_result.append(member)
            process_write_count = io_counters[1]
            member = {
                "metric": "process_write_count",
                "endpoint": endpoint,
                "timestamp": timestamp,
                "step": 60,
                "value": process_write_count,
                "counterType": "COUNTER",
                "tags": tags
            }
            process_result.append(member)
            process_read_bytes = io_counters[2]
            member = {
                "metric": "process_read_bytes",
                "endpoint": endpoint,
                "timestamp": timestamp,
                "step": 60,
                "value": process_read_bytes,
                "counterType": "COUNTER",
                "tags": tags
            }
            process_result.append(member)
            process_write_bytes = io_counters[3]
            member = {
                "metric": "process_write_bytes",
                "endpoint": endpoint,
                "timestamp": timestamp,
                "step": 60,
                "value": process_status,
                "counterType": "COUNTER",
                "tags": tags
            }
            process_result.append(member)

if __name__ == "__main__":
    main()
    print json.dumps(process_result, indent=2)
