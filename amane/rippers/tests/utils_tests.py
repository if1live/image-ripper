#-*- coding: utf-8 -*-

from __future__ import unicode_literals
import os
import unittest
from rippers import utils

class URLContentTest(unittest.TestCase):
    @unittest.skip
    def test_simple(self):
        url = 'http://libsora.so/robots.txt'
        url_content = utils.URLContent(url)
        self.assertEqual(len(url_content.text) > 0, True)
        self.assertEqual(len(url_content.data) > 0, True)

class FakeURLContentTest(unittest.TestCase):
    def test_simple(self):
        source = 'asdfqwer'
        url_content = utils.FakeURLContent('dummy-url', source)
        self.assertEqual(url_content.text, source)
        self.assertEqual(url_content.data, source)

    def test_create_from_file(self):
        filename = os.path.join(os.path.dirname(__file__), 'data', 'hello_world.txt')
        url_content = utils.FakeURLContent.create_from_file(filename)
        # damm windows newline policy + git newline!
        expected = [
            'hello world!\n',
            'hello world!\r\n'
        ]
        self.assertIn(url_content.text, expected)
