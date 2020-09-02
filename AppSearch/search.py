# -*- coding:utf-8 -*-
import sys
import threading

from workflow import Workflow3
from workflow import web

reload(sys)
sys.setdefaultencoding('utf8')


class SearchItme:
    def __init__(self, uid, name, no_content, url):
        self.uid = uid
        self.name = name
        self.no_content = no_content
        self.url = url
        self.icon = 'images/{0}.png'.format(name)


xclient = SearchItme('1', 'xclient', '没有找到内容', 'https://xclient.info/search/s/{0}')
macwk = SearchItme('2', 'macwk', '未查询到数据', 'https://www.macwk.com/soft/all/s-{0}/p1')
appked = SearchItme('3', 'appked', '0 Search results', 'https://www.macbed.com/?s={0}')
macapps = SearchItme('4', 'macapps', 'No Posts found', 'https://macapps.to/?s={0}')

_search_list = [xclient, appked, macapps, macwk]


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
    # Send output to Alfred. You can only call this once.
    # Well, you *can* call it multiple times, but subsequent calls
    # are ignored (otherwise the JSON sent to Alfred would be invalid).
    wf.send_feedback()


def _search(wf, item, query):
    url = item.url.format(query)
    subtitle = arg = url
    wf.logger.debug('--> ' + url)
    resp = web.get(url)
    wf.logger.debug('--> ' + resp.encoding)
    content = resp.text
    # wf.logger.debug(content)
    if content.count(item.no_content) > 0:
        wf.logger.debug('--> not result fund')
        subtitle = u'没有找到内容'
        # arg = None
    else:
        wf.add_item(item.name, subtitle=url, uid=item.uid,  icon=item.icon, arg=arg, valid=True)


if __name__ == '__main__':
    # Create a global `Workflow3` object
    wf = Workflow3()
    # Call your entry function via `Workflow3.run()` to enable its
    # helper functions, like exception catching, ARGV normalization,
    # magic arguments etc.
    wf.run(main)
    sys.exit()
