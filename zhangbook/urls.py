# -*- coding: utf-8 -*-
# __author__ = chenchiyuan
from __future__ import division, unicode_literals, print_function
from django.conf.urls import patterns, include, url
from views import get_all_books, get_book_detail, get_chapter_content, get_chapters

urlpatterns = patterns('',
    url(r'books/$', get_all_books, name="all_books"),
    url(r'book/detail/$', get_book_detail, name="book_detail"),
    url(r'chapters/$', get_chapters, name="chapters"),
    url(r'chapter/detail/$', get_chapter_content, name="chapter")
)
