#-*- coding: utf-8 -*-

import requests
from .helpers import to_unicode

class URLContent(object):
    global_referer = None
    global_cookie = None

    def __init__(self, url, *args, **kwargs):
        self.url = url
        self._request_cache = None
        self.referer = kwargs.pop('referer', None)
        self.cookie = kwargs.pop('cookie', None)

    @property
    def data(self):
        if not self._request_cache:
            self.run()
        return self._request_cache.content

    @property
    def text(self):
        content = self.data
        return to_unicode(content)

    @property
    def meta(self):
        if not self._request_cache:
            self.run()
        #TODO return http request meta data
        r = self._request_cache
        return r.headers

    def run(self):
        user_agent = ' '.join([
            'User-Agent:Mozilla/5.0 (Windows NT 6.3; WOW64)',
            'AppleWebKit/537.36 (KHTML, like Gecko)',
            'Chrome/39.0.2171.65 Safari/537.36'
        ])

        # TODO how to get cookie automatic?
        headers = {
            'Accept': 'image/webp,*/*;q=0.8',
            'User-agent': user_agent,
            'Accept-encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.6,en;q=0.4',
        }
        if self.referer:
            headers['Referer'] = self.referer
        if self.cookie:
            headers['Cookie'] = self.cookie

        cls = type(self)
        if cls.global_referer:
            headers['Referer'] = cls.global_referer
        if cls.global_cookie:
            headers['Cookie'] = cls.global_cookie

        r = requests.get(self.url, headers=headers)
        self._request_cache = r
        return r


class FakeURLContent(object):
    def __init__(self, url, source):
        self.url = url
        self._source = source

    @property
    def data(self):
        return self._source

    @property
    def text(self):
        content = self.data
        return to_unicode(content)


    @classmethod
    def create_from_file(cls, filename):
        with open(filename, 'rb') as f:
            content = f.read()
            return cls(filename, content)
