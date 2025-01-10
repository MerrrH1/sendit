from collections import OrderedDict
from rest_framework import pagination
from rest_framework.pagination import LimitOffsetPagination

class CustomPagination(LimitOffsetPagination):
    default_limit = 10
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    min_limit = 1
    max_limit = 50
    min_offset = 0
    max_offset = 10