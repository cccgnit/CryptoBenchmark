#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import datetime
import http.client
import mimetypes
import time

IP = "169.254.91.147"
PORT = 8000


def readCpuInfo():
    """
    Calculate system CPU usage
    :return: dict of CPU info
    """
    f = open('/proc/stat')
    lines = f.readlines()
    f.close()
    for line in lines:
        line = line.lstrip()
        counters = line.split()
        if len(counters) < 5:
            continue
        if counters[0].startswith('cpu'):
            break
    total = 0
    for i in range(1, len(counters)):
        total = total + int(counters[i])
    idle = int(counters[4])
    return {'total': total, 'idle': idle}


def calcCpuUsage(counters1, counters2):
    """
    Calculate system CPU usage
    :param counters1: dict, output of readCpuInfo()
    :param counters2: dict, output of readCpuInfo()
    :return: system CPU usage
    """
    idle = counters2['idle'] - counters1['idle']
    total = counters2['total'] - counters1['total']
    # return 100 - (idle*100/total)
    return 1 - (idle / total)


def readMemInfo():
    """
    Reqd system memory info
    :return: dict of info
    """
    res = {'total': 0, 'free': 0, 'buffers': 0, 'cached': 0}
    f = open('/proc/meminfo')
    lines = f.readlines()
    f.close()
    i = 0
    for line in lines:
        if i == 4:
            break
        line = line.lstrip()
        memItem = line.lower().split()
        if memItem[0] == 'memtotal:':
            res['total'] = int(memItem[1])
            i = i + 1
            continue
        elif memItem[0] == 'memfree:':
            res['free'] = int(memItem[1])
            i = i + 1
            continue
        elif memItem[0] == 'buffers:':
            res['buffers'] = int(memItem[1])
            i = i + 1
            continue
        elif memItem[0] == 'cached:':
            res['cached'] = int(memItem[1])
            i = i + 1
            continue
    return res


def calcMemUsage(counters):
    """
    Calculate system memory usage
    :param counters: dict, output of readMemInfo()
    :return: system memory usage
    """
    used = counters['total'] - counters['free'] - \
        counters['buffers'] - counters['cached']
    total = counters['total']
    # return used*100 / total
    return used / total


def readNetInfo(dev):
    """
    Read system network information
    :param dev: str, eth device ID
    :return: dict{'in': , 'out': }
    """
    f = open('/proc/net/dev')
    lines = f.readlines()
    f.close()
    res = {'in': 0, 'out': 0}
    for line in lines:
        if line.lstrip().startswith(dev):
            # for petalinux
            line = line.replace(':', ' ')
            items = line.split()
            res['in'] = int(items[1])
            res['out'] = int(items[int(len(items)/2) + 1])
    return res


def conn_django_test():
    """
    Connect django to test if it starts
    :return: bool
    """
    conn = http.client.HTTPConnection(IP, PORT)
    payload = ''
    headers = {
        'Content-Type': 'application/json'
    }
    # now = datetime.datetime.now()
    # timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    try:
        conn.request("GET", "", payload, headers)
        conn.getresponse()
        # print(timestamp+':', 'Now, Django 169.254.91.147:8000 is Open!')
        return True
    except:
        # print('\r'+timestamp+':', 'Django 169.254.91.147:8000 is Not Open!', end='')
        return False


def post_django(payload: str):
    """
    Request POST the cipher result to the django and mysql
    :param cipher_result: CipherResult 
    :return: the respose of django
    """
    conn = http.client.HTTPConnection(IP, PORT)
    headers = {
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/system/", payload, headers)
    res = conn.getresponse().read().decode("utf-8")
    return res


def generate_performance_payload(start_time, cpu_util_pct, mem_util_pct, net_info):
    """
    Request POST the cipher result to the django and mysql
    :param cipher_result: CipherResult 
    :return: payload
    """
    payload = "{\"startTime\":\"" + str(start_time) \
            + "\",\"cpuUtilPct\":\"" + '%0.4f' % cpu_util_pct \
            + "\",\"memUsedPct\":\"" + '%0.4f' % mem_util_pct \
            + "\",\"getTotal\":\"" + str(net_info['in']) \
            + "\",\"sentTotal\":\"" + str(net_info['out']) \
            + "\"}"
    return payload


def get_system_info():
    """
    Request POST the cipher result to the django and mysql 
    :return: payload
    """
    # get current time in UNIX timestamp
    start_time = int(time.time())
    # calculate system CPU usage
    counters1 = readCpuInfo()
    time.sleep(0.1)
    counters2 = readCpuInfo()
    cpu_util_pct = calcCpuUsage(counters1, counters2)
    # calculate system memory usage
    counters = readMemInfo()
    mem_util_pct = calcMemUsage(counters)
    # read system network information
    net_info = readNetInfo('eth0')
    # generate performance payload
    payload = generate_performance_payload(start_time, cpu_util_pct, mem_util_pct, net_info)
    # print(payload)
    return payload


if __name__ == '__main__':
    django_stat = conn_django_test()
    while True:
        payload = get_system_info()
        # print(payload)
        # send to the Django server
        if django_stat:
            res = post_django(payload)
            print(res)
        time.sleep(1)
