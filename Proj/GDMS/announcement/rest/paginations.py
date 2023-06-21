from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageiantion(PageNumberPagination):
    page_size = 10
    page_query_param = 'page'

    def get_paginated_response(self, data):
        res = {
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'results': data,
            'page': self.page.number
        }
        return Response(res)
