from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MyPage(PageNumberPagination):

    page_size = 5

    page_query_param = 'page'

    max_page_size = 10

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'results': data,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
        })
