#-*- coding: utf-8 -*-

from __future__ import unicode_literals
from __future__ import print_function

import zipfile
import os
import threading
import shutil
from .utils import URLContent
from . import core

class GalleryRipCommand(object):
    def __init__(self, mod, url):
        self.mod = mod
        self.url = url

        url_content = URLContent(url)
        doc = core.Document(url_content.text)
        self.gallery = mod.Gallery(doc)


    def get_output_zip_filepath(self):
        zip_filename = self.get_output_zip_filename()
        zip_filepath = os.path.join(self.get_output_zip_path(), zip_filename)
        return zip_filepath

    def get_output_zip_filename(self):
        zip_filename = '{}.zip'.format(self.gallery.get_filtered_title())
        return zip_filename

    def get_output_zip_path(self):
        curr_mod_path = os.path.dirname(__file__)
        output_path = os.path.join(curr_mod_path, '..', 'output')
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        return output_path

    def get_output_image_path(self):
        image_path = os.path.join(
            self.get_output_zip_path(),
            self.gallery.get_filtered_title()
        )
        return image_path

    def __call__(self):
        zip_filepath = self.get_output_zip_filepath()
        if os.path.exists(zip_filepath) and os.path.getsize(zip_filepath) > 1024:
            """
            not allow modify. so previous file is valid return value
            filesize=0 means you fail or occur bug.
            """
            return True

        pages = self.gallery.get_pages()
        total_page = len(pages)

        if total_page == 0:
            return False

        output_dir = self.get_output_image_path()
        # prepare download path
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # use thread to downaload parallel.
        threads = []

        NUM_WORKER = 4
        task_list = [[] for i in range(NUM_WORKER)]
        for i, page in enumerate(pages):
            idx = i % NUM_WORKER
            task_list[idx].append(page)

        for i, x in enumerate(task_list):
            t = ImageDownloadThread()
            t.reset_task(i, x, output_dir)
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

        self.create_zip()
        shutil.rmtree(output_dir)

        return True

    def create_zip(self):
        zip_filepath = self.get_output_zip_filepath()

        # only write, not allow append
        # because I don't need modifiable gallary such as deviantart.
        zip_args = 'w'
        zip_obj = zipfile.ZipFile(zip_filepath, zip_args)
        img_dir = self.get_output_image_path()
        for root, dirs, files in os.walk(self.get_output_image_path()):
            for f in files:
                filename = os.path.split(f)[1]
                zip_obj.write(os.path.join(img_dir, f), '/{}'.format(filename))
        zip_obj.close()

class ImageDownloadThread(threading.Thread):
    def reset_task(self, worker_id, pages, output_dir):
        self.worker_id = worker_id
        self.pages = pages
        self.output_dir = output_dir

    def run(self):
        for i, page in enumerate(self.pages):
            image = page.image
            image.save(self.output_dir)

            msg = '(%d:%d/%d) %s\n' % (self.worker_id, i + 1, len(self.pages), image.url)
            print(msg, end="")
