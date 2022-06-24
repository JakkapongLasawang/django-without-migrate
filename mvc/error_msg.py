import json


def error_msg(e):
    output = []

    errors = json.loads(e.json())

    for error in errors:
        output.append(
            {
                "field": error["loc"][0],
                "msg": error["msg"],
                # "type": error["type"].split(".")[1],
            }
        )
    return output
