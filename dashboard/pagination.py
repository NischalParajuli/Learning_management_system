"""Pagination classes for dashboard list views.

Provides pagination configuration for dashboard statistics and reporting.
"""

from rest_framework.pagination import PageNumberPagination


class AdminPagination(PageNumberPagination):
    """Pagination class for admin dashboard endpoints.
    
    Returns 10 items per page with a maximum page size of 50.
    """
    page_size = 10
    page_query_param = 'page_size'
    max_page_size = 50


class SponsorPagination(PageNumberPagination):
    """Pagination class for sponsor dashboard endpoints.
    
    Returns 10 items per page with a maximum page size of 50.
    """
    page_size = 10
    page_query_param = 'page_size'
    max_page_size = 50
  