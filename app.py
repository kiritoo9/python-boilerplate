import os
from dotenv import load_dotenv
from flask import Flask
from src.routes.welcome import welcome
from src.routes.v1.auth import auth

load_dotenv()
app = Flask(__name__)
app.register_blueprint(welcome, url_prefix="/")

# Version 1
app.register_blueprint(auth, url_prefix="/v1/auth")

if __name__ == "__main__":
    app.run(host=os.environ.get("APP_HOST"), port=os.environ.get("APP_PORT"), debug=True)