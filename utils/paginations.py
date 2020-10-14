from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class MyPage(PageNumberPagination):
    page_query_param = 'page'
    page_size_query_param = 'pagesize'
    max_page_size = 10
    page_size = 5

    def get_paginated_response(self, data):
        return Response({
            'count':self.page.paginator.count,
            'results':data,
        })
