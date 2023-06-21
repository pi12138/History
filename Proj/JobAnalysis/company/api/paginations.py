from rest_framework import pagination


class JobPositionPagination(pagination.PageNumberPagination):
    page_size = 10
    page_query_param = 'page'
