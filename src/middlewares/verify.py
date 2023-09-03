import os
import jwt
from dotenv import load_dotenv
from functools import wraps
from quart import request
from src.models.users import Users

load_dotenv()

def verifyToken(func):
    @wraps(func)
    async def decorated_function(*args, **kwargs):
        bearer = request.headers.get('Authorization')
        if bearer is None:
            return { "message": "Missing header authorization" }, 401

        token = bearer[7:]
        # Check valid JWT
        try:
            decoded = jwt.decode(token, os.environ.get("SECRET_KEY"), algorithms="HS256")
            # Check existing user
            user = Users.query.filter(Users.id == decoded.get("id")).filter(Users.deleted == False).first()
            if user is None:
                return { "message": "User is not found, probably token is expired already" }, 401
            else:
                return await func(*args, **kwargs)
        except Exception as e:
            return { "message": "Token is not valid" }, 401
            
        return { "message": "Authentication failed" }, 401

    return decorated_function