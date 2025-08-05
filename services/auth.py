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
    try:
        return User.query.get(int(user_id)) # type: ignore
    except Exception as e:
        logger.error(f"An error occured\n{e}")
        return None