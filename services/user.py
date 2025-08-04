
from models.users import User 
from core.database import db


def register_user(new_user: User):
    db.session.add(new_user)
    db.session.commit()
    db.session.refresh(new_user)  # type: ignore
    return new_user
