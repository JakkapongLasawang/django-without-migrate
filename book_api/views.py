import json
from django.views import View
from pydantic import ValidationError, parse_obj_as
from typing import List
from book_api.validators.book import CreateBook, UpdateBook, GetBook, DeleteBook
from book_api.models import Book
from mvc.decode_payload import decode_payload
from mvc.error_msg import error_msg
from mvc.response import js_response


OK = "OK"
NOT_JSON = "Invalid JSON"
INPUT_INVALID = "Invalid input"
CANNOT_CREATE = "Cannot Create"
CANNOT_UPDATE = "Cannot Update"
CANNOT_DELETE = "Cannot Delete"
NOT_FOUND = "Not Found"


class REST(View):
    def get(self, request):
        try:
            books = Book.objects.all().order_by('-published').values()
        except Book.DoesNotExist:
            return js_response(400, "Not Found")

        response = parse_obj_as(List[GetBook], list(books))
        return js_response(200, OK, response)

    def post(self, request):
        body = decode_payload(request.body)
        if body is None:
            return js_response(400, NOT_JSON)

        try:
            payload = CreateBook(**body).dict()
        except ValidationError as e:
            return js_response(400, INPUT_INVALID, error_msg(e))
        book = None
        try:
            book = Book.objects.create(**payload)
        except Exception:
            return js_response(400, CANNOT_CREATE)

        return js_response(201, OK, GetBook(**book.__dict__))

    def put(self, request):
        body = decode_payload(request.body)
        if body is None:
            return js_response(400, NOT_JSON)

        try:
            payload = UpdateBook(**body).dict()
        except ValidationError as e:
            return js_response(400, INPUT_INVALID, error_msg(e))

        book = None
        try:
            book = Book.objects.filter(id=payload['id'])
            if not book:
                return js_response(400, NOT_FOUND)
            del payload['id']
            book.update(**payload)
        except Exception:
            return js_response(400, CANNOT_UPDATE)

        return js_response(202, OK, GetBook(**book[0].__dict__))

    def delete(self, request):
        body = decode_payload(request.body)
        if body is None:
            return js_response(400, NOT_JSON)

        try:
            payload = DeleteBook(**body).dict()
        except ValidationError as e:
            return js_response(400, INPUT_INVALID, error_msg(e))
        try:
            Book.objects.filter(id=payload['id']).delete()
        except Exception:
            return js_response(400, CANNOT_DELETE)

        return js_response(204, OK)
