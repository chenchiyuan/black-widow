# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function

class BookSpiderInterface(object):
    def get_all_books(self, *args, **kwargs):
        """
        返回以书名为key的字典
        """

        raise NotImplemented

    def get_book_detail(self, *args, **kwargs):
        raise NotImplemented

    def get_chapters(self, name, *args, **kwargs):
        raise NotImplemented

    def get_chapter_content(self, *args, **kwargs):
        raise NotImplemented