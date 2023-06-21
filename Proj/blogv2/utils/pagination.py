from rest_framework import pagination
from rest_framework.response import Response

class CustomPagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        # 页码控制
        num_pages = self.page.paginator.num_pages
        number = self.page.number
        
        if num_pages < 5:
            num_page_list = range(1, num_pages+1)
        elif number <= 3:
            num_page_list = range(1, 6)
        elif num_pages - 3 < number:
            num_page_list = range(num_pages-4, num_pages+1)
        else:
            num_page_list = range(number-2, number+3)

        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'results': data,
            'num_pages': num_pages,
            'num_page_list': list(num_page_list),
            'number': number
        })