from datetime import date, timedelta
import pandas as pd

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView, LoginView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema

from .models import *
from .forms import *
from .serializers import (UserSerializer, BookSerializer, RequestSerializer, PublisherSerializer, AuthorSerializer,
                          GenreSerializer, LanguageSerializer, CommentSerializer, EvaluationSerializer)

# Authentication Views
class RegisterView(View):
    template_name = 'reg/registration.html'

    def get(self, request):
        form = UserForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('profile')
        return render(request, self.template_name, {'form': form})


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)


class CustomLoginView(LoginView):
    template_name = 'reg/login.html'
    authentication_form = AuthenticationForm
    next_page = 'home'


def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def home_view(request):
    books = Book.objects.filter(is_deleted=False, quantity__gt=0)
    return render(request, 'Books/book_list.html', {'books': books})

@login_required
def profile(request):
    user = request.user
    rented_books = Request.objects.filter(user=user, status__name='Pending')
    return render(request, 'profile.html', {'user': user, 'rented_books': rented_books})

# CRUD Views

class AuthorCreateView(CreateView):
    model = Author
    template_name = 'Authors/author_create.html'
    form_class = AuthorForm
    success_url = reverse_lazy('authors')


class AuthorListView(ListView):
    model = Author
    template_name = 'Authors/author_list.html'
    context_object_name = 'list_authors'
    paginate_by = 12
    extra_context = {'title': 'Авторы'}


class AuthorUpdateView(UpdateView):
    model = Author
    template_name = 'Authors/author_update.html'
    form_class = AuthorForm
    success_url = reverse_lazy('authors')


class AuthorDeleteView(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()
        return HttpResponseRedirect(self.success_url)


class GenreUpdateView(UpdateView):
    model = Genre
    template_name = 'Genres/genre_update.html'
    form_class = GenreForm
    success_url = reverse_lazy('genres')


class GenreDeleteView(DeleteView):
    model = Genre
    success_url = reverse_lazy('genres')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()
        return HttpResponseRedirect(self.success_url)


class BookUpdateView(UpdateView):
    model = Book
    template_name = 'Books/book_update.html'
    form_class = BookForm
    success_url = reverse_lazy('book_list')


class BookDeleteView(DeleteView):
    model = Book
    success_url = reverse_lazy('book_list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()
        return HttpResponseRedirect(self.success_url)


class PublisherCreateView(CreateView):
    model = Publisher
    template_name = 'Publishers/publisher_create.html'
    form_class = PublisherForm
    success_url = reverse_lazy('publishers')


class PublisherListView(ListView):
    model = Publisher
    template_name = 'Publishers/publisher_list.html'
    context_object_name = 'list_publishers'
    paginate_by = 12


class PublisherUpdateView(UpdateView):
    model = Publisher
    template_name = 'Publishers/publisher_update.html'
    form_class = PublisherForm
    success_url = reverse_lazy('publishers')


class PublisherDeleteView(DeleteView):
    model = Publisher
    success_url = reverse_lazy('publishers')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()
        return HttpResponseRedirect(self.success_url)


class LanguageCreateView(CreateView):
    model = Language
    template_name = 'Languages/language_create.html'
    form_class = LanguageForm
    success_url = reverse_lazy('languages')


class LanguageListView(ListView):
    model = Language
    template_name = 'Languages/language_list.html'
    context_object_name = 'list_languages'
    paginate_by = 12


class LanguageUpdateView(UpdateView):
    model = Language
    template_name = 'Languages/language_update.html'
    form_class = LanguageForm
    success_url = reverse_lazy('languages')


class LanguageDeleteView(DeleteView):
    model = Language
    success_url = reverse_lazy('languages')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()
        return HttpResponseRedirect(self.success_url)


class CommentCreateView(CreateView):
    model = Comment
    template_name = 'Comments/comment_create.html'
    form_class = CommentForm
    success_url = reverse_lazy('comments')


class CommentListView(ListView):
    model = Comment
    template_name = 'Comments/comment_list.html'
    context_object_name = 'list_comments'
    paginate_by = 12


class CommentUpdateView(UpdateView):
    model = Comment
    template_name = 'Comments/comment_update.html'
    form_class = CommentForm
    success_url = reverse_lazy('comments')


class CommentDeleteView(DeleteView):
    model = Comment
    success_url = reverse_lazy('comments')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()
        return HttpResponseRedirect(self.success_url)


class EvaluationCreateView(CreateView):
    model = Evaluation
    template_name = 'Evaluations/evaluation_create.html'
    form_class = EvaluationForm
    success_url = reverse_lazy('evaluations')


class EvaluationListView(ListView):
    model = Evaluation
    template_name = 'Evaluations/evaluation_list.html'
    context_object_name = 'list_evaluations'
    paginate_by = 12


class EvaluationUpdateView(UpdateView):
    model = Evaluation
    template_name = 'Evaluations/evaluation_update.html'
    form_class = EvaluationForm
    success_url = reverse_lazy('evaluations')


class EvaluationDeleteView(DeleteView):
    model = Evaluation
    success_url = reverse_lazy('evaluations')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()
        return HttpResponseRedirect(self.success_url)


class RequestCreateView(CreateView):
    model = Request
    template_name = 'Requests/request_create.html'
    form_class = RequestForm
    success_url = reverse_lazy('requests')


class RequestListView(ListView):
    model = Request
    template_name = 'Requests/request_list.html'
    context_object_name = 'list_requests'
    paginate_by = 12


class RequestUpdateView(UpdateView):
    model = Request
    template_name = 'Requests/request_update.html'
    form_class = RequestForm
    success_url = reverse_lazy('requests')


class RequestDeleteView(DeleteView):
    model = Request
    success_url = reverse_lazy('requests')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()
        return HttpResponseRedirect(self.success_url)


class AuthorsList(ListView):
    model = Author
    template_name = 'Authors/author_list.html'
    context_object_name = 'list_authors'
    paginate_by = 12
    extra_context = {'title': 'Авторы'}



class GenreCreateView(CreateView):
    model = Genre
    template_name = 'Genres/genre_create.html'
    form_class = GenreForm
    success_url = reverse_lazy('genres')

class GenresList(ListView):
    model = Genre
    template_name = 'Genres/genre_list.html'
    context_object_name = 'list_genres'
    paginate_by = 12
    extra_context = {'title': 'Жанры'}

class CommentsList(ListView):
    model = Comment
    template_name = 'Comments/comment_list.html'
    context_object_name = 'list_comments'
    paginate_by = 12
    extra_context = {'title': 'Комментарии'}

class EvaluationsList(ListView):
    model = Evaluation
    template_name = 'Evaluations/evaluation_list.html'
    context_object_name = 'list_evaluations'
    paginate_by = 12
    extra_context = {'title': 'Оценки'}

class LanguagesList(ListView):
    model = Language
    template_name = 'Languages/language_list.html'
    context_object_name = 'list_languages'
    paginate_by = 12
    extra_context = {'title': 'Языки'}

class PublishersList(ListView):
    model = Publisher
    template_name = 'Publishers/publisher_list.html'
    context_object_name = 'list_publishers'
    paginate_by = 12
    extra_context = {'title': 'Издатели'}

class RequestsList(ListView):
    model = Request
    template_name = 'Requests/request_list.html'
    context_object_name = 'list_requests'
    paginate_by = 12
    extra_context = {'title': 'Запросы'}


class BookCreateView(CreateView):
    model = Book
    template_name = 'Books/book_create.html'
    form_class = BookForm
    success_url = reverse_lazy('book_list')


class BookList(ListView):
    model = Book
    template_name = 'Books/book_list.html'
    context_object_name = 'list_books'
    paginate_by = 2

    def get_queryset(self):
        queryset = Book.objects.filter(is_deleted=False)
        form = BookFilterForm(self.request.GET)

        if form.is_valid():
            tag = form.cleaned_data.get('tag')
            category = form.cleaned_data.get('category')

            if category:
                queryset = queryset.filter(category=category)
            if tag:
                queryset = queryset.filter(tags=tag)

        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['form'] = BookFilterForm(self.request.GET)
        return context


# Utility Functions
def index(request):
    return render(request, 'index.html')


def book_list(request):
    books = Book.objects.filter(is_deleted=False)
    genres = Genre.objects.all()
    authors = Author.objects.all()
    selected_genre = request.GET.get('genre')
    selected_author = request.GET.get('author')

    if selected_genre:
        books = books.filter(genre__id=selected_genre)

    if selected_author:
        books = books.filter(author__id=selected_author)

    books = books.filter(quantity__gt=0)

    return render(request, 'Books/book_list.html', {'books': books, 'genres': genres, 'authors': authors, 'selected_genre': selected_genre, 'selected_author': selected_author})


class CustomPagination(PageNumberPagination):
    page_size = 1  # Количество объектов на странице
    page_size_query_param = 'page_size'
    max_page_size = 1000  # Максимальное количество объектов на странице



class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    pagination_class = CustomPagination


class CustomModelViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['patch'], url_path='delete-multiple')
    def delete_multiple(self, request):
        """
        Метод для множественного логического удаления объектов.

        Ожидается JSON-объект вида {"ids": [1, 2, 3, ...]}
        где ids - список идентификаторов объектов для удаления.
        """
        ids = request.data.get('ids', [])
        queryset = self.get_queryset().filter(id__in=ids)

        if not queryset.exists():
            return Response("No objects found with the provided IDs.", status=status.HTTP_404_NOT_FOUND)

        queryset.update(is_deleted=True)
        return Response("Objects successfully marked as deleted.", status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'], url_path='restore-multiple')
    def restore_multiple(self, request):
        """
        Метод для множественного восстановления объектов.

        Ожидается JSON-объект вида {"ids": [1, 2, 3, ...]}
        где ids - список идентификаторов объектов для восстановления.
        """
        ids = request.data.get('ids', [])
        queryset = self.get_queryset().filter(id__in=ids)

        if not queryset.exists():
            return Response("No objects found with the provided IDs.", status=status.HTTP_404_NOT_FOUND)

        queryset.update(is_deleted=False)
        return Response("Objects successfully restored.", status=status.HTTP_200_OK)


@extend_schema(tags=['Книги'])
class BookViewSet(CustomModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_queryset(self):
        return self.queryset.filter(is_deleted=False)

@extend_schema(tags=['Жанры'])
class GenreViewSet(CustomModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get_queryset(self):
        return self.queryset.filter(is_deleted=False)

@extend_schema(tags=['Авторы'])
class AuthorViewSet(CustomModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_queryset(self):
        return self.queryset.filter(is_deleted=False)

@extend_schema(tags=['Запросы'])
class RequestViewSet(viewsets.ModelViewSet):
    serializer_class = RequestSerializer
    queryset = Request.objects.all()
    pagination_class = CustomPagination


@extend_schema(tags=['Языки'])
class LanguageViewSet(viewsets.ModelViewSet):
    serializer_class = LanguageSerializer
    queryset = Language.objects.all()
    pagination_class = CustomPagination


@extend_schema(tags=['Издатели'])
class PublisherViewSet(viewsets.ModelViewSet):
    serializer_class = PublisherSerializer
    queryset = Genre.objects.all()
    pagination_class = CustomPagination


@extend_schema(tags=['Комментарии'])
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    pagination_class = CustomPagination


@extend_schema(tags=['Оценки'])
class EvaluationViewSet(viewsets.ModelViewSet):
    serializer_class = EvaluationSerializer
    queryset = Evaluation.objects.all()
    pagination_class = CustomPagination


def api(request):
    return render(request, 'api.html')


def export_books_to_excel(request):
    books = Book.objects.all()
    data = {
        'Title': [book.title for book in books],
        'Publication Year': [book.publication_year for book in books],
        'Author': [f"{book.author.first_name} {book.author.last_name}" for book in books],
        'Genre': [book.genre.name for book in books],
    }
    df = pd.DataFrame(data)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="books.xlsx"'
    df.to_excel(response, index=False)
    return response
