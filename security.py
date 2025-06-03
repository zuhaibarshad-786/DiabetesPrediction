from functools import wraps
from flask import request, jsonify
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_TOKEN = os.getenv("SECRET_TOKEN")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token') or request.form.get('token')
        if token != SECRET_TOKEN:
            return jsonify({'message': 'Invalid or missing token'}), 401
        return f(*args, **kwargs)
    return decorated
