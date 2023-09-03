import os
import bcrypt
import jwt
from dotenv import load_dotenv
from quart import Blueprint, request
from src.models.users import Users

load_dotenv()
auth = Blueprint('auth', __name__)

@auth.route("/login", methods=["POST"])
async def index():
    try:
        body = await request.json

        data = Users.query.filter(Users.username == body.get("username")).filter(Users.deleted == False).first()
        if data is None:
            return { "message": "User is not found" }, 400
        data = data.serialize()

        # Check hash password
        encoded_password = body.get("password").encode("utf-8")
        if bcrypt.checkpw(encoded_password, data.get("password").encode("utf-8")) is False:
            return { "message": "Username and password does not match" }, 401

        # Genearate Token
        payloads = {
            "id": str(data.get("id")),
            "fullname": data.get("fullname"),
            "role": "admin" # static data
        }
        encoded_jwt = jwt.encode(payloads, os.environ.get("SECRET_KEY"), algorithm="HS256")

        # Generate token and send response
        return {
            "message": "This is auth endpoint",
            "access_token": encoded_jwt
        }, 201
    except Exception as e:
        return(str(e))