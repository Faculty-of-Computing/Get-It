from dotenv import load_dotenv
import os
import logging
from flask_bcrypt import Bcrypt

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
# Go 2 levels up from configs.py (e.g., from core/configs.py to project root)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
UPLOAD_FOLDER = os.path.join(BASE_DIR,'static','uploads')
# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
DEBUG=os.getenv("DEBUG") == "True"
SECRET_KEY= os.getenv("SECRET_KEY")


class ColoredFormatter(logging.Formatter):
    COLORS = {
        "DEBUG": "\033[94m",   #NOTE Blue
        "INFO": "\033[92m",    #NOTE  Green 
        "WARNING": "\033[93m", #NOTE Yellow
        "ERROR": "\033[91m",   #NOTE Red
        "CRITICAL": "\033[1;91m", # Bold Red
    }
    RESET = "\033[0m"

    def format(self, record):
        log_color = self.COLORS.get(record.levelname, self.RESET)
        record.levelname = f"{log_color}{record.levelname}{self.RESET}"
        return super().format(record)

# Configure logger
logger = logging.getLogger("colored_logger")
logger.setLevel(logging.DEBUG)

# Create handler
handler = logging.StreamHandler()
handler.setFormatter(ColoredFormatter("%(levelname)s:     %(funcName)s:Line-%(lineno)d: %(message)s"))

# Add handler to logger
logger.addHandler(handler)

bycrypt = Bcrypt()

print("Configs Loaded Successfully: ", DATABASE_URL)