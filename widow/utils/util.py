# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
import hashlib
from datetime import datetime as py_time
from django.utils.timezone import make_aware, get_default_timezone, is_naive, now
from datetime import timedelta
import const

def md5(input):
    m = hashlib.md5()
    m.update(input)
    return m.hexdigest()

def number2chinese(number):
    number_map = {
        "0": "0",
        "1": "一",
        "2": "二",
        "3": "三",
        "4": "四",
        "5": "五",
        "6": "六",
        "7": "七",
        "8": "八",
        "9": "九"
    }
    digit = ["", "十", "百", "千", "万", "十", "百", "千"]
    text = str(number)
    digits = digit[:len(text)]
    reverse_text = map(lambda x: number_map.get(x, "0"), text[::-1])
    match = zip(reverse_text, digits)
    if match[-1][0] == "0":
        match = match[:-1]
    result = map(lambda x: x[0] + x[1] if x[0] != "0" else '零', match[::-1])
    return "".join(result)

def datetime_to_str(datetime, format=const.DATETIME_FORMAT):
    if is_naive(datetime): # datetime to utc time
        datetime = to_aware_datetime(datetime)

    return datetime.strftime(format)

def datetime_delta(datetime, **kwargs):
    delta = timedelta(**kwargs)
    return datetime - delta

def str_to_datetime(str, format=const.DATETIME_FORMAT):
    if isinstance(str, py_time):
        if is_naive(str):
            return to_aware_datetime(str)
        else:
            return str

    return to_aware_datetime(py_time.strptime(str, format))

def to_aware_datetime(value):
    time_zone = get_default_timezone()
    return make_aware(value, time_zone)

def datetime_now():
    return now()
