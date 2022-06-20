from rest_framework.pagination import PageNumberPagination


class ArticlesAPIListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'paginate_by'
    max_page_size = 50
