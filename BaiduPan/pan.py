#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import sys


def get_code(s):
    ret = re.search(r'(密码|提取码)(:|：)?(.*)', s)
    if ret:
        code = ret.group(3)
        return code.strip()


def get_url(s):
    ret = re.search(r'链接(:|：)?(.*)(密码|提取码)(:|：)?(.*)', s)
    if ret:
        url = ret.group(2)
        url = url.replace(';', "")
        return url.strip()
    return s


if __name__ == '__main__':
    args = sys.argv
    s = args[1]
    # s = '链接：https://pan.baidu.com/s/1IKmrXnkRgk3lm-sdo11-FQ ;提取码：v080'
    # s = '链接:https://pan.baidu.com/s/1ovpiovI1HivWgv8a87zlPw 密码:1nqp'
    url = ''
    code = ''
    prefx = 'https://pan.baidu.com/s/'
    ret = re.search(r'(\w{4}\s*帝国DG)', s)
    if ret:
        code = ret.group()
        code = re.sub(r'\s+帝国DG', '', code)
        ret = re.search(r'◎帝.+国(.*)◎文件格式', s)
        if ret:
            url = ret.group()
            url = re.sub(r'[\s　帝国◎文件格式]+', '', url)
            url = prefx + url.split('/')[-1]
    else:
        url = get_url(s)
        code = get_code(s)
    if prefx not in url:
        url = prefx + url
    if code:
        url = '{0}#{1}'.format(url, code)
    print url
