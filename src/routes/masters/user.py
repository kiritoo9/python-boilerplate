import bcrypt
import datetime
import math
from quart import Blueprint, jsonify, request
from marshmallow import Schema, fields, validate, ValidationError, validates_schema
from src.helpers.help import get_args
from src.helpers.upload import upload
from src.middlewares.verify import verifyToken
from src.businesses.user import getUsers, getUserCount, getUserById, getUserByUsername, insertUser, updateUser

user = Blueprint('user', __name__)

class UserSchema(Schema):
    id = fields.UUID(require=False)
    username = fields.Str(required=True)
    password = fields.Str(required=False)
    fullname = fields.Str(required=True)
    photo = fields.Str(required=False)

    @validates_schema
    def validate_password(self, data, **kwargs):
        if 'id' not in data and 'password' not in data or 'id' not in data and data.get("password") == "":
            raise ValidationError("Password cannot be empty")


@user.route("/", methods=["GET"])
@verifyToken
async def index():
    try:
        args = await get_args([
            {
                "name": "foo",
                "default_value": "bar"
            } # custom query parameters
        ])

        data = await getUsers(args)
        totalPage = 1
        count = await getUserCount(args)
        if count > 0 and args.get("limit") > 0:
            totalPage = math.ceil(count / args.get("limit"))

        args["totalPage"] = totalPage
        return {
            "args": args,
            "data": data
        }, 200
    except Exception as e:
        return {
            "message": "Something went wrong",
            "detail": str(e)
        }, 400

@user.route("/<uuid:id>", methods=["GET"])
@verifyToken
async def detail(id):
    data = await getUserById(id)
    if data is None:
        return { "message": "Data is not found" }, 400

    return {
        "message": f"Request success with id {id}",
        "data": data.serialize()
    }, 200

@user.route("/", methods=["POST"])
@verifyToken
async def create():
    body = await request.json

    # Validate input
    try:
        body = UserSchema().load(body)
    except ValidationError as err:
        return {
            "message": "Validation error",
            "detail": err.messages
        }, 400
    
    # Validate existing and insert data
    exists = await getUserByUsername(body.get("username"))
    if exists is not None:
        return { "message": "Username is already exists" }, 400

    # Example when there is something needs to upload (image or file)
    if body.get("photo") != "":
        uploadResponse = await upload(body.get("photo"), "users")
        if uploadResponse.get("uploaded") is False:
            return { "message": uploadResponse.get("message") }, 400
        else:
            # Condition when upload file is success
            print(f'Your file uploaded in here -> {uploadResponse.get("filename")}')

    # Hash password
    encoded_password = body.get("password").encode("utf-8")
    password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())

    data = {
        "id": None, # set None, uuid will set default in database
        "username": body.get("username"),
        "password": password.decode("utf-8"),
        "fullname": body.get("fullname"),
        "created_date": datetime.datetime.now()
    }
    result = await insertUser(data)
    if result.get("success") == False:
        return { "message": result.get("message") }, 400

    # Response
    return {
        "message": "Data inserted",
    }, 201
    
@user.route("/", methods=["PUT"])
@verifyToken
async def update():
    body = await request.json

    # Validate input
    try:
        body = UserSchema().load(body)
    except ValidationError as err:
        return {
            "message": "Validation error",
            "detail": err.messages
        }, 400

    data = await getUserById(body.get("id"))
    if data is None:
        return { "message": "Data is not found" }, 404

    # Check exsiting username
    user = await getUserByUsername(body.get("username"), body.get("id"))
    if user is None:
        user = await getUserByUsername(body.get("username"))
        if user is not None:
            return { "message": "Username is already exists" }, 400

    data = {
        "username": body.get("username"),
        "fullname": body.get("fullname"),
    }

    # Hash password
    if body.get("password") != "":
        encoded_password = body.get("password").encode("utf-8")
        password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())
        data["password"] = password.decode("utf-8")

    # Update user
    result = await updateUser(body.get("id"), data)
    if result.get("success") == False:
        return { "message": result.get("message") }, 400

    return { "message": "Data updated" }, 201

@user.route("/<uuid:id>", methods=["DELETE"])
@verifyToken
async def remove(id):
    user = await getUserById(id)
    if user is None:
        return { "message": "Data is not found" }, 404

    result = await updateUser(id, {"deleted": True})
    if result.get("success") == False:
        return { "message": result.get("message") }, 400

    return { "message": "Data deleted" }, 201