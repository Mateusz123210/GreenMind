from app import plants_models, users_models
from app.decorators.plants_database_decorator import plants_db
from app.decorators.users_database_decorator import users_db

@users_db
def get_user_by_email(email, users_db):
    return users_db.query(users_models.User).filter(users_models.User.email == email).first()

@users_db
def get_user_tokens(user, users_db):
    return users_db.query(users_models.Token).filter(users_models.Token.user_id == user.uuid).all()

@plants_db
def get_plantation(uuid, plants_db):
    return plants_db.query(plants_models.Plant).filter(plants_models.Plant.uuid == uuid).first()