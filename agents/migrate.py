from flask import Flask
from flask_migrate import Migrate
from src.configs.database import DB

app = Flask(__name__)
migrate = Migrate(app, DB)