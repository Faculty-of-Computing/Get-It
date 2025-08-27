from core.configs import ALLOWED_EXTENSIONS,logger
from wtforms.validators import ValidationError
import re
from cloudinary.utils import cloudinary_url

def validate_phone(form, field):
    phone = field.data.strip()

    # Example: Allow Nigerian numbers like 08012345678 or +2348012345678
    pattern = re.compile(r"^(?:\+234|0)[789][01]\d{8}$")

    if not pattern.match(phone):
        raise ValidationError("Enter a valid Nigerian phone number.")
    
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

