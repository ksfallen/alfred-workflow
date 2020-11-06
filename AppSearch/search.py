# -*- coding:utf-8 -*-
import re
import sys

import threading

from workflow import Workflow3
from workflow import web

reload(sys)
sys.setdefaultencoding('utf8')

_headers = {
    'cookie': "__cfduid=d44abbc23076c9ccc86f541cf69552d601598427403; theme_mode=light; cf_chl_prog=a19; cf_clearance=116038be755d8034532b1c01deb20349120e82b2-1599102352-0-1za7bda3ffz77534c4fz611be4a7-250",
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
}


class SearchItme:
    def __init__(self, uid, name, url, no_content, reg=''):
        self.uid = uid
        self.name = name
        self.content = no_content
        self.no_content = no_content
        self.reg = reg
        self.url = url
        self.icon = 'images/{0}.png'.format(name)
        self.post = False
        self.param = {}


xclient = SearchItme('1', 'xclient', 'https://xclient.info/search/s/{0}', '没有找到内容')
macwk = SearchItme('2', 'macwk', 'https://www.macwk.com/soft/all/s-{0}/p1', '未查询到数据')
macdrop = SearchItme('3', 'macdrop', 'https://macdrop.net/?s={0}&asl_active=1&p_asid=1', 'No results were found for this query')
appked = SearchItme('4', 'appked', 'https://www.macbed.com/?s={0}', '0 Search results', '\\d+ Search results')
macapps = SearchItme('5', 'macapps', 'https://macapps.to/?s={0}', 'No Posts found')
_search_list = [xclient, appked, macdrop, macwk]
# _search_list = [macdrop]


def main(wf):
    # The Workflow3 instance will be passed to the function
    # you call from `Workflow3.run`.
    # Not super useful, as the `wf` object created in
    # the `if __name__ ...` clause below is global...
    #
    # Your imports go here if you want to catch import errors, which
    # is not a bad idea, or if the modules/packages are in a directory
    # added via `Workflow3(libraries=...)`
    # import anothermodule

    # Get args from Workflow3, already in normalized Unicode.
    # This is also necessary for "magic" arguments to work.
    args = wf.args

    # Do stuff here ...

    # Add an item to Alfred feedback
    # wf.add_item(u'Item title', u'Item subtitle')
    if args:
        query = ' '.join(args)
        threads = []
        for itme in _search_list:
            t = threading.Thread(target=_search, args=(wf, itme, query))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
    else:
        wf.add_item('输入关键字', '等待查询')
    wf.warn_empty('没有找到内容', icon='icon.png')

    # Send output to Alfred. You can only call this once.
    # Well, you *can* call it multiple times, but subsequent calls
    # are ignored (otherwise the JSON sent to Alfred would be invalid).
    wf.send_feedback()


def _search(wf, item, query):
    item = _get_web_data(wf, item, query)
    uid = item.uid
    url = item.url
    content = item.content
    arg = subtitle = url
    if item.reg:
        ret = re.search(re.compile(item.reg), content)
        no_result = ret and ret.group() == item.no_content
    else:
        no_result = content.count(item.no_content) > 0
    if no_result:
        wf.logger.info('--> not result fund:' + item.no_content + ', name:' + item.name)
        # wf.logger.debug('--> content:' + content)
        subtitle = u'没有找到内容'
        arg = None
        # uid = '99'
    wf.add_item(query, subtitle, arg, uid=uid, icon=item.icon, valid=True)


def _get_web_data(wf, item, query):
    url = item.url.format(query)
    timeout = 8
    try:
        if item.post:
            param = _param_to_dic(item.param.format(query))
            resp = web.post(url, param, headers=_headers, timeout=timeout)
        else:
            resp = web.get(url, headers=_headers, timeout=timeout)
            wf.logger.debug('--> ' + url + ' charset=' + resp.encoding)
        item.content = resp.text
        item.url = url
    except Exception as e:
        wf.logger.error("--> http error:" + url + " msg:" + e.message, exc_info=e)
    return item


def _param_to_dic(param):
    ret = {}
    items = param.split('&')
    for item in items:
        value = item.split('=')
        ret.setdefault(value[0], value[1])
    return ret


if __name__ == '__main__':
    # Create a global `Workflow3` object
    wf = Workflow3()
    # 测试
    wf.alfred_env['debug'] = 1
    # Call your entry function via `Workflow3.run()` to enable its
    # helper functions, like exception catching, ARGV normalization,
    # magic arguments etc.
    wf.run(main)
    sys.exit()
