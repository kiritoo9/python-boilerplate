import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

# Init functions
load_dotenv()
DB = SQLAlchemy()

# Default Database
DB_HOST = os.environ.get("DB_HOST")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME")
CONNECTION_STRING = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"