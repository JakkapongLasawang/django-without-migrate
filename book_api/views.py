import json
from django.views import View
from pydantic import ValidationError, parse_obj_as
from typing import List
from book_api.validators.book import CreateBook, UpdateBook, GetBook, DeleteBook
from book_api.models import Book
from mvc.decode_payload import decode_payload
from mvc.error_msg import error_msg
from mvc.response import js_response


class REST(View):
    def get(self, request):
        try:
            books = Book.objects.all().order_by('-published').values()
        except Book.DoesNotExist:
            return js_response(400, "Not Found", {})

        response = parse_obj_as(List[GetBook], list(books))
        return js_response(0, "OK", response)

    def post(self, request):
        body = decode_payload(request.body)
        if body is None:
            return js_response(400, "Invalid JSON", {})

        try:
            payload = CreateBook(**body).dict()
        except ValidationError as e:
            return js_response(400, "Input not valid", error_msg(e))
        book = None
        try:
            book = Book.objects.create(**payload)
        except Exception:
            return js_response(400, "Cannot create book", {})

        return js_response(0, "success", GetBook(**book.__dict__))

    def put(self, request):
        body = decode_payload(request.body)
        if body is None:
            return js_response(400, "Invalid JSON", {})

        try:
            payload = UpdateBook(**body).dict()
        except ValidationError as e:
            return js_response(400, "Input not valid", error_msg(e))

        book = None
        try:
            book = Book.objects.filter(id=payload['id'])
            del payload['id']
            book.update(**payload)
        except Exception:
            return js_response(400, "Cannot update book", {})

        return js_response(0, "success", GetBook(**book[0].__dict__))

    def delete(self, request):
        body = decode_payload(request.body)
        if body is None:
            return js_response(400, "Invalid JSON", {})

        try:
            payload = DeleteBook(**body).dict()
        except ValidationError as e:
            return js_response(400, "Input not valid", error_msg(e))
        try:
            Book.objects.filter(id=payload['id']).delete()
        except Exception:
            return js_response(400, "Cannot delete", {})

        return js_response(0, "success", {})
