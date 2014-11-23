#-*- coding: utf-8 -*-

import urlparse
import core
from .helpers import HtmlHelper
from .utils import URLContent
from .cmds import GalleryRipCommand
import os

NAME = 'naver'
TAGS = ['naver',]

class Base(core.Base):
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

class NaverMetaDataStragety(core.BaseMetaDataStrategy):
    def get_title(self):
        helper = HtmlHelper(self.doc)
        return helper.get_meta('og:title')

def is_naver_webtoon(url):
    url_data = urlparse.urlparse(url)
    is_host_naver = url_data.netloc == 'comic.naver.com'
    is_path_naver_webtoon = url_data.path == '/webtoon/detail.nhn'
    return is_host_naver and is_path_naver_webtoon

def handle_url(url):
    url_data = urlparse.urlparse(url)
    # http://comic.naver.com/webtoon/detail.nhn?titleId=81482&no=544&weekday=tue
    if url_data.path == '/webtoon/detail.nhn':
        return handle_detail_page(url)

def handle_detail_page(url):
    from importd import d

    mod = core.get_site_module(NAME)
    URLContent.global_referer = url
    cmd = GalleryRipCommand(mod, url)
    success = cmd()
    URLContent.global_referer = None
    if not success:
        msg = 'download failed: %s %s' % (site, uid)
        return d.HttpResponse(msg)

    filepath = cmd.get_output_zip_filepath()
    filename = cmd.get_output_zip_filename()
    data = open(filepath, 'rb').read()
    resp = d.HttpResponse(data, content_type='application/x-zip')
    resp['Content-Disposition'] = 'attachment; filename="{}"'.format(filename).encode('utf-8')
    resp['Content-Length'] = os.path.getsize(filepath)
    return resp


def create_url_filter_list():
    IGNORE_HOST_LIST = [
        'adcreative.naver.com',
    ]

    filter_list = [
        core.ImageURLFilterPolicy_NoGif(),
        core.ImageURLFilterPolicy_NoThumbnail(),
        core.ImageURLFilterPolicy_IgnoreHostName(IGNORE_HOST_LIST),
        core.ImageURLFilterPolicy_AllowCommonHostName(),
    ]
    return filter_list

class Board(core.Board, Base):
    pass

class Gallery(core.Gallery, Base):
    def __init__(self, doc):
        core.Gallery.__init__(self, doc, create_url_filter_list())
        self.metadata_strategy = NaverMetaDataStragety(self.doc)

class Page(core.Page, Base):
    pass

class Image(core.Image, Base):
    pass


def register():
    core.site_detector.register(NAME, is_naver_webtoon)
