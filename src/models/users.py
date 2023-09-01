import uuid
from sqlalchemy.dialects.postgresql import UUID
from src.configs.database import DB

class Users(DB.Model):
    __tablename__ = 'users'

    id = DB.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = DB.Column(DB.String())
    password = DB.Column(DB.String())
    fullname = DB.Column(DB.String())
    deleted = DB.Column(DB.Boolean(), default=False)
    created_date = DB.Column(DB.DateTime(timezone=True))

    def __init__(self, id, username, password, fullname, created_date):
        self.id = id
        self.username = username
        self.password = password
        self.fullname = fullname
        self.created_date = created_date

    def serialize(self):
        return {
            'id': self.id, 
            'username': self.username,
            'password': self.password,
            'fullname':self.fullname,
            'created_date':self.created_date
        }