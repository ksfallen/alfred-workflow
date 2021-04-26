#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re
import sys

if __name__ == '__main__':
    args = sys.argv
    s = args[1]
    url = code = ''
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
        ret = url + '#' + code
    if '链接' in s and '密码' in s:
        # 链接:https://pan.baidu.com/s/1ovpiovI1HivWgv8a87zlPw 密码:1nqp
        s = re.sub(r'\s*密码:', '#', s)
        url = s.replace('链接:', '')
        ret = url.strip()
    else:
        ret = prefx + s
    print ret
