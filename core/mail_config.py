import os
# Flask-Mail SMTP configuration for production
MAIL_SERVER =os.getenv("SMTP_HOST")  # Or your SMTP provider
MAIL_PORT = os.getenv("SMTP_PORT")
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = os.getenv('USERNAME')
MAIL_PASSWORD = os.getenv('PASSWORD')
MAIL_DEFAULT_SENDER = os.getenv('SEND_FROM')
