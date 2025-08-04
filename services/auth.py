from flask_login import LoginManager # type: ignore
from models.users import User
from core.database import db


login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id:int)->User|None:
    user = db.session.execute(db.select(User).where(User.id==user_id)).scalars().one_or_none()
    return user