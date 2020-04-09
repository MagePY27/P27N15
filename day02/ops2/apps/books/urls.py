from django.urls import path, include
from apps.books import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'publisher_action', views.PublisherViewSet)
router.register(r'author_action', views.AuthorViewSet)
router.register(r'book_action', views.BookViewSet)

app_name = 'books'

urlpatterns = [
    # drf
    path('', include(router.urls), name='books-publisher_action'),
    # publisher
    path('publisher/', views.PublishView.as_view(), name='books-publisher'),
    path('publisher/create/', views.PublishCrateView.as_view(), name='books-publisher-create'),
    path('publisher/update/', views.PublishUpdateView.as_view(), name='books-publisher-update'),
    # author
    path('author/', views.AuthorView.as_view(), name='books-author'),
    path('author/create/', views.AuthorCrateView.as_view(), name='books-author-create'),
    path('author/update/', views.AuthorUpdateView.as_view(), name='books-author-update'),
    # books
    path('books/', views.BooksView.as_view(), name='books-books'),
]

