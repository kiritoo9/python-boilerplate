import os
from dotenv import load_dotenv
from quart import Quart
from src.configs.database import CONNECTION_STRING, DB
from src.routes.welcome import welcome
from src.routes.auth import auth
from src.routes.masters.user import user

load_dotenv()
app = Quart(__name__)

# Connect to database
app.config['SQLALCHEMY_DATABASE_URI'] = CONNECTION_STRING
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB.init_app(app)

# Regist Routes
app.register_blueprint(welcome, url_prefix="/")
app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(user, url_prefix="/master/user")

# Error handler
@app.errorhandler(404)
async def not_found(e):
    return {
        "message": "Route is not found, make sure you update our documentation"
    }, 404

if __name__ == "__main__":
    debug = False
    if os.environ.get("APP_ENV") == "dev":
        debug = True
    app.run(host=os.environ.get("APP_HOST"), port=os.environ.get("APP_PORT"), debug=debug)