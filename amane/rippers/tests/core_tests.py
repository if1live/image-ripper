#-*- coding: utf-8 -*-

import unittest
from .helpers import get_document, get_data_filepath
import rippers
from rippers import core
"""
class GalleryTest(unittest.TestCase):
    def test_naver_webtoon_basic(self):
        doc = get_document('naver-webtoon-basic.html')
        gallery = rippers.Gallery(doc)
        expected_title = '놓지마 정신줄 - 525화 아빠와 행복한 오후'
        self.assertEqual(gallery.get_title(), expected_title)
        self.assertEqual(1, len(gallery.get_pages()))
"""

def is_dummy_func(doc):
    return True

class SiteDetectorTest(unittest.TestCase):
    def test_test(self):
        detector = core.SiteDetector()
        detector.register('dummy', is_dummy_func)
        self.assertEqual('dummy', detector.detect('fake'))

    def test_double_register(self):
        detector = core.SiteDetector()
        detector.register('dummy', is_dummy_func)
        try:
            detector.register('dummy', is_dummy_func)
            self.fail()
        except RuntimeError:
            pass

class register_site_Test(unittest.TestCase):
    def setUp(self):
        core.site_detector.reset()

    def test_register(self):
        self.assertEqual(0, len(core.site_detector))
        core.register_site('rippers.naver')
        self.assertEqual(1, len(core.site_detector))

class ImageURLFitlerPolicy_NoGif_Test(unittest.TestCase):
    def test_run(self):
        policy = core.ImageURLFilterPolicy_NoGif()
        self.assertEqual(False, policy.check_url('asdf.gif'))
        self.assertEqual(False, policy.check_url('ASDF.GIF'))
        self.assertEqual(True, policy.check_url('asdf.txt'))

class ImageURLFitlerPolicy_NoThumbnail_Test(unittest.TestCase):
    def test_run(self):
        policy = core.ImageURLFilterPolicy_NoThumbnail()
        self.assertEqual(True, policy.check_url('test.png'))
        self.assertEqual(False, policy.check_url('thumb_test.png'))

class ImageURLFitlerPolicy_IgnoreHostName_Test(unittest.TestCase):
    def test_run(self):
        ignore_list = ['google.com', 'fake.com']
        policy = core.ImageURLFilterPolicy_IgnoreHostName(ignore_list)
        self.assertEqual(True, policy.check_url('http://pass.com/asdf.png'))
        self.assertEqual(False, policy.check_url('http://google.com/asdf.png'))
        self.assertEqual(False, policy.check_url('http://fake.com/asdf.png'))

class ImageURLFitlerPolicy_AllowComonHostName(unittest.TestCase):
    def test_run(self):
        url_list = [
            'http://google.com/a.png',
            'http://google.com/b.png',
            'http://test.com/c.png',
            'http://google.com/d.png'
        ]
        policy = core.ImageURLFilterPolicy_AllowCommonHostName()
        actual = policy(url_list)
        expected = [
            'http://google.com/a.png',
            'http://google.com/b.png',
            'http://google.com/d.png'
        ]
        self.assertEqual(3, len(actual))
        self.assertEqual(expected, actual)


    def test_similary(self):
        input_data = {
            'cfile25.uf.tistory.com': 3,
            'cfile30.uf.tistory.com': 2,
            'cfile23.uf.tistory.com': 1,
            'cfile24.uf.tistory.com': 2,
            'cfile8.uf.tistory.com': 2,
            'cfile5.uf.tistory.com': 3,
            'cfile4.uf.tistory.com': 1,
            'cfile22.uf.tistory.com': 2,
            'cfile27.uf.tistory.com': 2,
            'cfile28.uf.tistory.com': 1,
            'cfile21.uf.tistory.com': 1,
            'cfile2.uf.tistory.com': 3,
            'cfile26.uf.tistory.com': 1,
            'cfile10.uf.tistory.com': 1,
            'cfile7.uf.tistory.com': 3,
            'i1.daumcdn.net': 3,
        }

        expected = [
            'cfile25.uf.tistory.com',
            'cfile30.uf.tistory.com',
            'cfile23.uf.tistory.com',
            'cfile24.uf.tistory.com',
            'cfile8.uf.tistory.com',
            'cfile5.uf.tistory.com',
            'cfile4.uf.tistory.com',
            'cfile22.uf.tistory.com',
            'cfile27.uf.tistory.com',
            'cfile28.uf.tistory.com',
            'cfile21.uf.tistory.com',
            'cfile2.uf.tistory.com',
            'cfile26.uf.tistory.com',
            'cfile10.uf.tistory.com',
            'cfile7.uf.tistory.com',
        ]

        policy = core.ImageURLFilterPolicy_AllowCommonHostName()
        actual = policy.find_common_hostname_list_from_count_table(url_list)
        self.assertEqual(set(actual), set(expected))
