from flask import request
from functools import wraps

# simple API key (you can change this)
API_KEY = "123456"

def require_api_key(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        key = request.headers.get("x-api-key")

        if key != API_KEY:
            return {"message": "Unauthorized"}, 401

        return func(*args, **kwargs)

    return wrapper
