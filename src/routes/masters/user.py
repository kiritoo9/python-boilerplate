from quart import Blueprint, jsonify
from src.models.users import Users
from src.helpers.help import get_args

user = Blueprint('user', __name__)

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
    try:
        data = Users.query\
            .filter(Users.id == id)\
            .filter(Users.deleted == False)\
            .one()

        return {
            "message": f"Request success with id {id}",
            "data": data.serialize()
        }, 200
    except Exception as e:
        return {
            "message": "Something went wrong",
            "detail": str(e)
        }, 400