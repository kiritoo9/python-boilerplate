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
            .filter(Users.deleted == False)\
            .limit(args.get("limit"))\
            .offset(args.get("offset"))\
            .all()

        return {
            "success": True,
            "args": args,
            "data": [v.serialize() for v in result]
        }, 200
    except Exception as e:
        return(str(e))