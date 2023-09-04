from src.models.users import Users
from src.configs.database import DB
from sqlalchemy.exc import SQLAlchemyError

async def getUsers(args):
    filters = [Users.deleted == False]

    # Add search filter
    if args.get("keywords") != "":
        filters.append(Users.fullname.ilike(f'%{args.get("keywords")}%'))

    result = Users.query\
        .with_entities(Users.id, Users.fullname)\
        .filter(*filters)\
        .limit(args.get("limit"))\
        .offset(args.get("offset"))\
        .all()
    
    data = []
    for v in result:
        data.append({
            "id": v.id,
            "fullname": v.fullname
        })
    
    return data

async def getUserCount(args):
    filters = [Users.deleted == False]

    # Add search filter
    if args.get("keywords") != "":
        filters.append(Users.fullname.ilike(f'%{args.get("keywords")}%'))

    return Users.query\
        .filter(*filters)\
        .count()

async def getUserById(id):
    return Users.query\
        .filter(Users.id == id)\
        .filter(Users.deleted == False)\
        .first()

async def getUserByUsername(username, id = None):
    query = Users.query\
        .filter(Users.username == username)\
        .filter(Users.deleted == False)

    if id is not None:
        query.filter(Users.id == id)

    return query.first()

async def insertUser(data):
    try:
        to_insert = Users(**data)
        DB.session.add(to_insert)
        DB.session.commit()
        return { "message": "Insert success", "success": True }
    except SQLAlchemyError as err:
        DB.session.rollback()
        errorMessage = str(err.__dict__['orig'])
        return { "message": errorMessage, "success": False }

async def updateUser(id, data):
    try:
        Users.query.filter(Users.id == id).update(data, synchronize_session = False)
        DB.session.commit()
        return { "message": "Update success", "success": True }
    except SQLAlchemyError as err:
        DB.session.rollback()
        errorMessage = str(err.__dict__['orig'])
        return { "message": errorMessage, "success": False }