#  Copyright © 2022., Brainergy Co., Ltd. All rights reserved.

import json

from django.http import HttpResponse


def js_response(code, message, result):
    jsr = JsonResponse(code, message, result)
    response = HttpResponse(jsr.to_json())
    response["Content-Type"] = "application/json"
    return response


class JsonResponse:
    def __init__(self, code, message, result):
        self.code = str(code)
        self.message = str(message) if message is not None else None
        self.result = result

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)
