from quart import Blueprint, jsonify, request
from src.models.users import Users
from src.configs.database import DB
from src.helpers.help import get_args
from marshmallow import Schema, fields, validate, ValidationError
import bcrypt
from sqlalchemy.exc import SQLAlchemyError

user = Blueprint('user', __name__)

class UserCreatedSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6, max=40))
    fullname = fields.Str(required=True)

@user.route("/", methods=["GET"])
async def index():
    try:
        args = await get_args([
            {
                "name": "foo",
                "default_value": "bar"
            } # custom query parameters
        ])

        result = Users.query\
            .with_entities(Users.id, Users.fullname)\
            .filter(Users.deleted == False)\
            .limit(args.get("limit"))\
            .offset(args.get("offset"))\
            .all()

        data = []
        for v in result:
            data.append({
                "id": v.id,
                "fullname": v.fullname
            })

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
async def detail(id):
    data = Users.query\
        .filter(Users.id == id)\
        .filter(Users.deleted == False)\
        .first()

    if data is None:
        return { "message": "Data is not found" }, 400

    return {
        "message": f"Request success with id {id}",
        "data": data.serialize()
    }, 200

@user.route("/", methods=["POST"])
async def create():
    body = await request.json

    # Validate input
    try:
        body = UserCreatedSchema().load(body)
    except ValidationError as err:
        return {
            "message": "Validation error",
            "detail": err.messages
        }, 400
    
    # Validate existing and insert data
    exists = Users.query\
        .filter(Users.username == body.get("username"))\
        .filter(Users.deleted == False)\
        .first()
    if exists is not None:
        return { "message": "Username is already exists" }, 400

    try:
        # Hash password
        encoded_password = body.get("password").encode("utf-8")
        password = bcrypt.hashpw(encoded_password, bcrypt.gensalt())

        # Do insert
        to_insert = Users(None, body.get("username"), password.decode("utf-8"), body.get("fullname"), None)
        DB.session.add(to_insert)
        DB.session.commit()
    except SQLAlchemyError as err:
        DB.session.rollback()
        errorMessage = str(err.__dict__['orig'])
        return { "message": errorMessage }, 400

    # Response
    return {
        "message": "Data inserted",
    }, 201
    