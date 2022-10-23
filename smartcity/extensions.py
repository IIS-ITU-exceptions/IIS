# from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

# migrate = Migrate()
login_manager = LoginManager()
db = SQLAlchemy()

