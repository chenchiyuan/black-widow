# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from django.http import HttpResponse
import json

json_response = lambda data: HttpResponse(json.dumps(data), content_type="application/json")