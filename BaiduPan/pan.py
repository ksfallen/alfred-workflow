#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import sys

if __name__ == '__main__':
    args = sys.argv
    s = args[1]
    url = code = ''
    ret = re.search(r'(\w{4}\s*帝国DG)', s)
    if ret:
        code = ret.group()
        code = re.sub(r'\s+帝国DG', '', code)
    ret = re.search(r'◎帝.+国(.*)◎文件格式', s)
    if ret:
        url = ret.group()
        url = re.sub(r'[\s　帝国◎文件格式]+', '', url)
        url = url.split('/')[-1]
        # print url
    print url + '#' + code
