"""Pagination classes for course list views.

Provides pagination configuration for large course result sets.
"""

from rest_framework.pagination import PageNumberPagination


class CoursePagination(PageNumberPagination):
    """Pagination class for course list endpoints.
    
    Returns 10 courses per page with a maximum page size of 50.
    """
    page_size = 10
    page_query_param = 'page_size'
    max_page_size = 50