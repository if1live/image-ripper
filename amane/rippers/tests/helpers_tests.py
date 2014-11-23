#-*- coding: utf-8 -*-

from __future__ import unicode_literals

import unittest
from rippers import helpers

class filter_title_Test(unittest.TestCase):
    def test_protected(self):
        title = 'Protected: 아카메가 벤다! 51화'
        expected = '아카메가_벤다!_51화'
        self.assertEqual(helpers.filter_title(title), expected)

    def test_not_vaild_character(self):
        title = 'a:b/c|d,e'
        expected = 'a-b-c-d-e'
        self.assertEqual(helpers.filter_title(title), expected)

    def test_whitespace(self):
        title = ' 가 나 다 '
        expected = '가_나_다'
        self.assertEqual(helpers.filter_title(title), expected)
