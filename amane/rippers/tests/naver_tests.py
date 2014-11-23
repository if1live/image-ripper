#-*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

import unittest
import rippers
from rippers import naver
from rippers.tests.helpers import get_document, read_line_text

class is_naver_webtoon_Test(unittest.TestCase):
    def test_run(self):
        url = 'http://comic.naver.com/webtoon/detail.nhn?titleId=81482&no=544&weekday=tue'
        self.assertEqual(True, naver.is_naver_webtoon(url))

class NaverMetaDataStragetyTest(unittest.TestCase):
    def test_data(self):
        doc = get_document('naver-webtoon-basic.html')

        strategy = naver.NaverMetaDataStragety(doc)
        expected_title = '놓지마 정신줄 - 525화 아빠와 행복한 오후'
        actual_title = strategy.get_title()
        self.assertEqual(expected_title, actual_title)

class NaverGalleryURLTest(unittest.TestCase):
    def get_page_urls(self, filename):
        doc = get_document(filename)
        page = rippers.Gallery(doc, naver.create_url_filter_list())
        image_urls = page.get_page_urls()
        return image_urls

    def test_naver_webtoon_basic(self):
        actual = self.get_page_urls('naver-webtoon-basic.html')
        expected = read_line_text('naver-webtoon-basic-expected.txt')
        self.assertEqual(actual, expected)

    def test_naver_webtoon_smart_toon(self):
        actual = self.get_page_urls('naver-webtoon-smart-toon.html')
        expected = read_line_text('naver-webtoon-smart-toon-expected.txt')
        self.assertEqual(actual, expected)
