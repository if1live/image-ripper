#-*- coding: utf-8 -*-

import core
import os
from .utils import URLContent
from .helpers import HtmlHelper
from .cmds import GalleryRipCommand

NAME = 'general'
TAGS = ['general',]

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

def create_url_filter_list():
    filter_list = [
        core.ImageURLFilterPolicy_NoGif(),
        core.ImageURLFilterPolicy_NoThumbnail(),
        core.ImageURLFilterPolicy_AllowCommonHostName(),
    ]
    return filter_list

def is_general(url):
    return True

def handle_url(url):
    from importd import d

    mod = core.get_site_module(NAME)
    cmd = GalleryRipCommand(mod, url)
    success = cmd()
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

class GeneralMetaDataStragety(core.BaseMetaDataStrategy):
    def get_title(self):
        helper = HtmlHelper(self.doc)
        og_title = helper.get_meta('og:title')
        if og_title:
            return og_title

        title_list = self.doc.find_all('title')
        for x in title_list:
            return x.text

class Board(core.Board, Base):
    pass

class Gallery(core.Gallery, Base):
    def __init__(self, doc):
        core.Gallery.__init__(self, doc, create_url_filter_list())
        self.metadata_strategy = GeneralMetaDataStragety(self.doc)

class Page(core.Page, Base):
    pass

class Image(core.Image, Base):
    pass

def register():
    core.site_detector.register(NAME, is_general)
