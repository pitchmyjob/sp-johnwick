from apps.core.api.pagination import CustomCursorPagination


class SpitchPagination(CustomCursorPagination):
    page_size = 8
