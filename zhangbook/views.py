# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from widow.utils.https import json_response
from zhangbook.spiders import ZhangBookSpider
import json

@csrf_exempt
def get_all_books(request):
    spider = ZhangBookSpider()
    kwargs = json.loads(request.body)
    data = spider.get_all_books(**kwargs)
    return json_response(data)

@csrf_exempt
def get_book_detail(request):
    kwargs = json.loads(request.body)
    spider = ZhangBookSpider()
    data = spider.get_book_detail(**kwargs)
    return HttpResponse(data)

@csrf_exempt
def get_chapters(request):
    spider = ZhangBookSpider()
    kwargs = json.loads(request.body)
    data = spider.get_chapters(**kwargs)
    return HttpResponse(data)

@csrf_exempt
def get_chapter_content(request):
    spider = ZhangBookSpider()
    kwargs = json.loads(request.body)
    data = spider.get_chapter_content(**kwargs)
    return HttpResponse(data)

