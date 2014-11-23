#-*- coding: utf-8 -*-

import os
import rippers
from rippers.utils import FakeURLContent

def get_data_filepath(filename):
    filepath = os.path.join(
        os.path.dirname(__file__),
        'data',
        filename
    )
    return filepath

def get_document(filename):
    filepath = get_data_filepath(filename)
    url_content = FakeURLContent.create_from_file(filepath)
    source = url_content.text
    return rippers.Document(source)


def read_line_text(filename):
    filepath = get_data_filepath(filename)
    line_list = []
    with file(filepath, 'rb') as f:
        for line in f:
            line_list.append(line.strip())
    line_list = [x for x in line_list if len(x) > 0]
    return line_list
