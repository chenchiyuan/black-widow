# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from django.conf import settings

# DATABASES
DB_SHORT_LENGTH = 16
DB_MIDDLE_LENGTH  = 32
DB_NAME_LENGTH = 128
DB_TIME_LENGTH = 128
DB_URL_LENGTH = 256
DB_CONTENT_LENGTH = 256*256*12*12
DB_DESCRIPTION_LENGTH = 256*24
DB_NUMBER_DEFAULT = 0

# CHOICES
UPDATE_BY_TIME = 0
UPDATE_STRATEGY_CHOICES = (
    (UPDATE_BY_TIME, u"time"),
)

# URL CONFIG
URL_BOOK_ID = "(?P<book_id>[0-9]+)"
URL_CHAPTER_ID = "(?P<chapter_id>[0-9]+)"
URL_ID = "(?P<id>[0-9]+)"

# SPIDERS
SPIDER_BASE_PATH = settings.SPIDER_BASE_DIR
SPIDER_HASH = 200
SPIDER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.7a) Gecko/20050614 Firefox/0.9.0+"
}

# CONTENT SIMILARITY
SIMILARITY_RATIO = 0.85

# DATETIME_FORMAT
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"
STRATEGY_TIME_FORMAT = "%H:%M"
DATETIME_FORMAT = "%s %s" %(DATE_FORMAT, TIME_FORMAT)