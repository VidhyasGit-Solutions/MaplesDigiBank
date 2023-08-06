from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from loguru import logger
import secrets

# Replace with your MySQL credentials and database name
DATABASE_NAME = "maple_digi_bank"
MYSQL_USERNAME = "root"
MYSQL_HOST = "localhost"
MYSQL_PASSWORD = "password"

app = Flask(__name__, instance_relative_config=True)
app.config["SECRET_KEY"] = "testing"
app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{DATABASE_NAME}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Generate a secure secret key
secret_key = secrets.token_hex(16)
app.secret_key = secret_key

log_file = "app.log"  # Specify the path and filename for the log file
logger.add(log_file, rotation="500 MB", retention="30 days", level="DEBUG")

def register(app):
    from maples_digi_app.application.views import applications
    from maples_digi_app.login.views import logins
    from maples_digi_app.creditcheck.views import creditchecks

    app.register_blueprint(logins)
    app.register_blueprint(applications)
    app.register_blueprint(creditchecks)

register(app)

with app.app_context():
    db.create_all()


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    from maples_digi_app.login.models import User

    return User.query.get(int(user_id))
