import json
from django.views import View
from .models import Book
from mvc.response import js_response


class REST(View):
    def get(self, request):
        try:
            books = Book.objects.all()
        except Book.DoesNotExist:
            return js_response(400, "Not Found", {})

        book_list = []
        for book in books:
            jsr = {
                "id": book.id,
                "title": book.title,
                "number_of_pages": book.number_of_pages,
                "quantity": book.quantity,
                "published": str(book.published),
            }
            book_list.append(jsr)

        return js_response(0, "success", book_list)

    def post(self, request):
        body = json.loads(request.body.decode("utf-8"))
        try:
            title = body["title"]
            number_of_pages = body["number_of_pages"]
            author = body["author"]
            quantity = body["quantity"]
        except Exception:
            return js_response(400, "Input not valid", {})

        book = None
        try:
            book = Book.objects.create(
                title=title,
                number_of_pages=number_of_pages,
                author=author,
                quantity=quantity,
            )
        except Exception:
            return js_response(400, "Cannot create book", {})

        jsr = {
            "id": book.id,
            "title": book.title,
        }
        return js_response(0, "success", jsr)
    
    def put(self, request):
        body = json.loads(request.body.decode("utf-8"))
        try:
            id = body["id"]
            title = body["title"]
            number_of_pages = body["number_of_pages"]
            author = body["author"]
            quantity = body["quantity"]
        except Exception:
            return js_response(400, "Input not valid", {})
        
        book = None
        try:
            book = Book.objects.filter(id=id)
            book.update(title=title,
                number_of_pages=number_of_pages,
                author=author,
                quantity=quantity,)
        except Exception:
            return js_response(400, "Cannot update book", {})
        
        jsr = {
                "id": book[0].id,
                "title": book[0].title,
                "number_of_pages": book[0].number_of_pages,
                "quantity": book[0].quantity,
                "published": str(book[0].published),
            }
        
        return js_response(0, "success", jsr)
    
    def delete(self, request):
        body = json.loads(request.body.decode("utf-8"))
        try:
            id = body["id"]
        except Exception:
            return js_response(400, "Input not valid", {})
        try:
            Book.objects.filter(id=id).delete()
        except Exception:
            return js_response(400, "Cannot delete", {})
        
        return js_response(0, "success", {})