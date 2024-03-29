from collections import OrderedDict
from rest_framework.response import Response
from rest_framework import pagination


class CustomPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response(
            OrderedDict([('count', self.page.paginator.count),
                         ('page_size', self.page_size),
                         ('page', self.page.number),
                         ('next', self.get_next_link()),
                         ('previous', self.get_previous_link()),
                         ('results', data)]))
