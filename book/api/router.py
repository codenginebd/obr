from rest_framework import routers
from book.api.viewsets.category_api_view import BookCategoryAPIView

book_router = routers.DefaultRouter()

book_router.register(r'^api/v1/category-list/$', BookCategoryAPIView)

