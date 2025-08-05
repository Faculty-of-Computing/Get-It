from flask_login import LoginManager # type: ignore
from models.users import User
from core.database import db
from urllib.parse import urlparse, urljoin
from core.configs import logger

def url_has_allowed_host_and_scheme(target, host_url):
    ref_url = urlparse(host_url)
    test_url = urlparse(urljoin(host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id:int)->User|None:
    user:User = db.session.execute(db.select(User).where(User.id==user_id)).scalars().one_or_none() # type: ignore
    logger.info(f'User:{user.username} Fecthed from the database')
    return user