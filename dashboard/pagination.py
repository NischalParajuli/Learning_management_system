from rest_framework.pagination import PageNumberPagination


class AdminPagination(PageNumberPagination):
  page_size = 10
  page_query_param = 'page_size'
  max_page_size = 50


class SponsorPagination(PageNumberPagination):
  page_size = 10
  page_query_param = 'page_size'
  max_page_size = 50
  