#-*- coding: utf-8 -*-

import os
import urlparse
from bs4 import BeautifulSoup
import helpers
import utils
import importlib

class Base(object):
    @property
    def Board(self):
        return Board
    @property
    def Gallery(self):
        return Gallery
    @property
    def Page(self):
        return Page
    @property
    def Image(self):
        return Image

class Document(object):
    def __init__(self, source):
        self.source = source
        self.soup = BeautifulSoup(source, 'html5lib')

class Board(Base):
    def __init__(self, doc):
        self.doc = doc


class Gallery(Base):
    def __init__(self, doc, filter_list=None):
        self.doc = doc
        self.metadata_strategy = None

        if not filter_list:
            filter_list = []
        self.filter_list = filter_list

    def get_title(self):
        return self.metadata_strategy.get_title()

    def get_filtered_title(self):
        return helpers.filter_title(self.get_title())

    def get_pages(self):
        raise NotImplementedError()

    def get_page_urls(self):
        # find image pattern
        soup = self.doc.soup
        img_list = soup.find_all('img')
        url_list = []
        for el in img_list:
            url_list.append(el['src'])
        url_list = [x for x in url_list if len(x) > 0]

        for policy in self.filter_list:
            url_list = policy(url_list)

        return url_list

    def get_pages(self):
        pages = []
        for idx, url in enumerate(self.get_page_urls()):
            url_content = utils.URLContent(url)
            page = self.Page(url_content, idx + 1)
            pages.append(page)
        return pages

class Page(Base):
    def __init__(self, url_content, num):
        self.url_content = url_content
        self.num = num

    @property
    def image(self):
        return self.Image(self.url_content, self.num)


class Image(Base):
    def __init__(self, url_content, num):
        assert type(url_content) not in (str, unicode)
        self.url_content = url_content
        self.num = num

    @property
    def url(self):
        return self.url_content.url

    @property
    def data(self):
        return self.url_content.data

    def get_meta(self, key):
        meta = self.url_content.meta
        return meta[key]

    @property
    def name(self):
        # check extension
        extension = os.path.splitext(self.url)[1].lower()
        if extension in ('.jpg', '.jpeg'):
            target_ext = '.jpg'
        elif extension in ('.png', '.gif'):
            target_ext = extension
        else:
            # if extension is not exist, use content-type
            content_type = self.get_meta('Content-Type')
            if content_type in ('image/jpeg',):
                target_ext = '.jpg'
            else:
                raise AssertionError('not supported image extension : %s' % (self.url,))

        return '%03d%s' % (self.num, target_ext)

    def save(self, output_dir):
        filepath = os.path.join(output_dir, self.name)
        with open(filepath, 'wb') as f:
            f.write(self.data)

class ImageURLFilterPolicy(object):
    """
    for finding most common hostname, use url_list not url.
    """
    def __call__(self, url_list):
        try:
            url_list = [x for x in url_list if self.check_url(x)]
            return url_list
        except NotImplementedError as e:
            raise e

    def check_url(self, url):
        raise NotImplementedError()

class ImageURLFilterPolicy_NoGif(ImageURLFilterPolicy):
    """
    ignore gif. maybe it is bullet or etc, not cartoon image.
    """
    def check_url(self, url):
        is_gif = lambda x: '.gif' == x.lower()[-4:]
        return not is_gif(url)


class ImageURLFilterPolicy_NoThumbnail(ImageURLFilterPolicy):
    """
    ignore thumbnail. this is not cartoon
    """
    def check_url(self, url):
        is_thumb = lambda x: 'thumb' in x.lower()
        return not is_thumb(url)

class ImageURLFilterPolicy_IgnoreHostName(ImageURLFilterPolicy):
    """
    ignore predefined host
    """

    def __init__(self, ignore_host_list):
        self.ignore_host_list = ignore_host_list

    def check_url(self, url):
        result = urlparse.urlparse(url)
        return result.netloc not in self.ignore_host_list

class ImageURLFilterPolicy_AllowCommonHostName(ImageURLFilterPolicy):
    """
    remove not common host.
    allow only one most common hostname.

    Sometimes, allow many hostname. Find similary hostname then allow all.
    cfile25.uf.tistory.com
    cfile30.uf.tistory.com
    cfile23.uf.tistory.com
    ....
    """
    def build_hostname_table(self, url_list):
        hostname_count_table = {}
        for url in url_list:
            result = urlparse.urlparse(url)
            hostname = result.netloc
            if hostname not in hostname_count_table:
                hostname_count_table[hostname] = 0
            hostname_count_table[hostname] += 1
        return hostname_count_table

    def find_common_hostname_list_from_count_table(self, table):
        candidate_list = table.keys()
        retval = []
        for hostname in candidate_list:
            if '.uf.tistory.com' in hostname:
                retval.append(hostname)
        return retval

    def find_common_hostname_list(self, url_list):
        hostname_count_table = self.build_hostname_table(url_list)
        return self.find_common_hostname_list_from_count_table(hostname_count_table)

    def __call__(self, url_list):
        hostname_list = self.find_common_hostname_list(url_list)
        is_allow_host = lambda x: urlparse.urlparse(x).netloc in hostname_list
        url_list = [x for x in url_list if is_allow_host(x)]
        return url_list

class BaseMetaDataStrategy(object):
    def __init__(self, doc):
        self.doc = doc

    def get_title(self):
        raise NotImplementedError()

class SiteDetector(object):
    def __init__(self):
        self.reset()

    def register(self, name, func):
        for item in self._func_list:
            if item[0] == name:
                raise RuntimeError('already registered')
        self._func_list.append((name, func))

    def detect(self, doc):
        for name, func in self._func_list:
            if func(doc):
                return name
        return None

    def __len__(self):
        return len(self._func_list)

    def reset(self):
        self._func_list = []

site_detector = SiteDetector()
site_mod_cache = {}

def register_site(mod_path):
    mod = importlib.import_module(mod_path)
    register_func = getattr(mod, 'register')
    register_func()

    site_mod_cache[mod.NAME] = mod
    return True

def get_site_module(name):
    return site_mod_cache[name]
