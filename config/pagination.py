from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import math


class ModifiedPageNumberPagination(PageNumberPagination):
    # http://127.0.0.1:8001/api/v1/supplement_events?page=last
    last_page_strings = ('last', )
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'last_page': self.get_last_page_number(self.page.paginator.count),
            'results': data,
            'current_page': self.page.number
        })

    def get_last_page_number(self, count):
        if not count:
            return None

        return math.ceil(count / self.page_size)
