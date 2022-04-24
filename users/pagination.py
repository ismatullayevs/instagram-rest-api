from rest_framework import pagination


class CursorPagination(pagination.CursorPagination):
    page_size = 30
    ordering = '-date_joined'
