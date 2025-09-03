from functools import wraps
from core.configs import ALLOWED_EXTENSIONS,logger
from wtforms.validators import ValidationError
import re
from flask_login import current_user
from flask import abort

def validate_phone(form, field):
    phone = field.data.strip()

    # Example: Allow Nigerian numbers like 08012345678 or +2348012345678
    pattern = re.compile(r"^(?:\+234|0)[789][01]\d{8}$")

    if not pattern.match(phone):
        raise ValidationError("Enter a valid Nigerian phone number.")
    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function