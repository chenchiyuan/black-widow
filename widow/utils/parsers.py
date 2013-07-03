# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from bs4 import BeautifulSoup
from xml.etree import cElementTree as ET

class SoupHelper(object):
    @classmethod
    def get_soup(cls, content):
        return BeautifulSoup(content, "lxml")

    @classmethod
    def get_root(cls, content):
        soup = cls.get_soup(content)
        return ET.fromstring(str(soup))