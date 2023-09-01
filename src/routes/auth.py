from quart import Blueprint, request
import bcrypt
from src.models.users import Users

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

        # Generate token and send response
        return {
            "message": "This is auth endpoint",
        }, 201
    except Exception as e:
        return(str(e))