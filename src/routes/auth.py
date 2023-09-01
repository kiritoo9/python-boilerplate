from quart import Blueprint

auth = Blueprint('auth', __name__)

@auth.route("/", methods=["POST"])
async def index():
    try:
        return {
            "message": "This is auth endpoint",
        }, 201
    except Exception as e:
        return(str(e))