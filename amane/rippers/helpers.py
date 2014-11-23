#-*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

from HTMLParser import HTMLParser

def filter_title(title):
    assert type(title) == unicode

    title = title.strip()

    MARUMARU_PROTECTED_PREFIX = 'Protected: '
    if MARUMARU_PROTECTED_PREFIX in title:
        title = title.replace(MARUMARU_PROTECTED_PREFIX, '')

    INVALID_CHARACTER_LIST = ":/|,?"
    for x in INVALID_CHARACTER_LIST:
        title = title.replace(x, '-')

    title = title.replace(' ', '_')

    try:
        title = utils.unescape()
    except:
        pass

    assert ' ' not in title
    assert type(title) == unicode
    return title

def to_unicode(val):
    if type(val) == unicode:
        return val

    elif type(val) == str:
        try:
            return val.decode('utf-8')
        except UnicodeDecodeError:
            return val.decode('euc-kr')
    else:
        raise AssertionError('not valid type')

def unescape(val):
    parser = HTMLParser()
    return parser.unescape(val)


class HtmlHelper(object):
    def __init__(self, doc):
        self.doc = doc

    def get_meta(self, key):
        meta_list = self.doc.soup.find_all('meta')
        for el in meta_list:
            if not el.has_attr('property'):
                continue
            if el['property'] == key:
                return el['content']
        return None
