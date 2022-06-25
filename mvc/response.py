#  Copyright © 2022., Brainergy Co., Ltd. All rights reserved.
import json
from django.http import HttpResponse


def js_response(code=200, msg=None, result={}):
    jsr = JsonResponse(code, msg, result)
    response = HttpResponse(jsr.to_json(), status=code)
    response["Content-Type"] = "application/json"
    return response


class JsonResponse:
    def __init__(self, code, msg, result):
        self.code = str(code)
        self.msg = str(msg) if msg is not None else None
        self.result = result

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=2)
