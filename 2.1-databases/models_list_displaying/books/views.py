from django.shortcuts import redirect
from django.views.generic import ListView, DayArchiveView, DetailView

from .models import Book


def index_view(request):
    return redirect('books')


class BookList(ListView):
    model = Book
    template_name = 'books/books_list.html'
    context_object_name = 'books'


class BookDateList(DayArchiveView):
    year_format = '%Y'
    month_format = '%m'
    day_format = '%d'
    queryset = Book.objects.all()
    template_name = 'books/books_by_date.html'
    date_field = 'pub_date'
    context_object_name = 'books'


class BookDetail(DetailView):
    model = Book
    template_name = 'books/book.html'
