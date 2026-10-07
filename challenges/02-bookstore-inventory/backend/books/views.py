"""
Bookstore inventory endpoints.

Product requirements (read carefully):
- CRUD for books: title, author, isbn, price, category, stock.
- List supports optional filters:
  - category: case-insensitive exact match
  - q: match title OR author (icontains)
- Update must persist all provided fields, including price.
"""

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Book
from .serializers import BookSerializer


@api_view(["GET"])
def health(request):
    return Response({"status": "ok", "challenge": "bookstore-inventory"})


@api_view(["GET", "POST"])
def list_or_create_books(request):
    if request.method == "POST":
        return create_book(request)
    return list_books(request)


def list_books(request):
    qs = Book.objects.all()

    category = (request.GET.get("category") or "").strip()
    q = (request.GET.get("q") or "").strip()

    if q:
        qs = qs.filter(title__icontains=q)

    return Response(BookSerializer(qs.order_by("title"), many=True).data)


def create_book(request):
    serializer = BookSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)
    book = serializer.save()
    return Response(BookSerializer(book).data, status=201)


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == "GET":
        return Response(BookSerializer(book).data)

    if request.method == "DELETE":
        book.delete()
        return Response(status=204)

    return update_book(request, book)


def update_book(request, book):
    data = request.data or {}

    if "title" in data:
        book.title = data["title"]
    if "author" in data:
        book.author = data["author"]
    if "isbn" in data:
        book.isbn = data["isbn"]
    if "category" in data:
        book.category = data["category"]
    if "stock" in data:
        try:
            book.stock = int(data["stock"])
        except (TypeError, ValueError):
            return Response({"error": "stock must be an integer"}, status=400)

    book.save()
    return Response(BookSerializer(book).data)
