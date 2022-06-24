import json

def decode_payload(payload):
    try:
        return json.loads(payload.decode("utf-8"))
    except Exception:
        return None
