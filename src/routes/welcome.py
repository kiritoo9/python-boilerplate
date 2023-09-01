from quart import Blueprint

welcome = Blueprint('welcome', __name__)

@welcome.route("/", methods=["GET"])
async def index():
    try:
        return {
            "message": "Welcome to MpuPython",
            "version": 1.0
        }, 200
    except Exception as e:
        return(str(e))