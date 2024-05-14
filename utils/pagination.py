from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class ExtendedPagination(PageNumberPagination):
    page_size = 5

    def get_paginated_response(self, data):
        return Response(
            {
                "count": self.page.paginator.count,
                "num_pages": self.page.paginator.num_pages,
                "page_number": self.page.number,
                "page_size": self.page_size,
                "next_link": self.get_next_link(),
                "previous_link": self.get_previous_link(),
                "results": data,
            }
        )
