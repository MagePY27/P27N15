from apps.books.models import Publisher, Book, Author
from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse
from utils.My_rest_viewset import MyViewBase
from .serializer import BookSerializer, PublisherSerializer, AuthorSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView


class PublishView(APIView):

    def get(self, request):
        city_list = Publisher.objects.values('city').distinct()
        return render(request, 'publisher.html', locals())


class PublishCrateView(APIView):

    def get(self, request):
        return render(request, 'publisher_create.html')


class PublishUpdateView(APIView):

    def get(self, request):
        if request.GET['id']:
            publisher = Publisher.objects.filter(id=request.GET['id']).first()

        return render(request, 'publisher_update.html', locals())


# class PublisherViewSet(viewsets.ModelViewSet):
class PublisherViewSet(MyViewBase):

    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    # filter
    filter_fields = ['city']
    # search
    search_fields = ('name', 'address')


# author
class AuthorView(APIView):

    def get(self, request):
        return render(request, 'author.html')


class AuthorViewSet(MyViewBase):

    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    # search
    search_fields = ('name', 'email')


class AuthorCrateView(APIView):

    def get(self, request):
        return render(request, 'author_create.html')


class AuthorUpdateView(APIView):

    def get(self, request):
        if request.GET['id']:
            author = Author.objects.filter(id=request.GET['id']).first()

        return render(request, 'author_update.html', locals())


# book
class BooksView(APIView):

    def get(self, request):
        return render(request, 'books.html')


class BookViewSet(MyViewBase):

    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookCreateView(APIView):

    def get(self, request):
        pub_list = Publisher.objects.all()
        author_list = Author.objects.all()
        return render(request, 'books_create.html', locals())






