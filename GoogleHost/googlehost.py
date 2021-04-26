#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys

import requests

reload(sys)
sys.setdefaultencoding('utf-8')


def read():
    ret = []
    hsot_flie = '/etc/hosts'
    with open(hsot_flie, mode='r') as f:
        line = f.read()
        ret.append(line)
        if '# GoogleHosts Start' in line:
            return ret
    return ret


def get_google_hosts():
    try:
        url = 'https://raw.githubusercontent.com/googlehosts/hosts/master/hosts-files/hosts'
        resp = requests.get(url, timeout=10).text
        hosts = resp.split('\n')
        index = hosts.index('# GoogleHosts Start')
        if index > 0:
            return hosts[index:]
    except:
        pass


if __name__ == '__main__':
    hosts = read()
    google_host = get_google_hosts()
    if google_host:
        hosts += google_host
    print '\n'.join(hosts)
