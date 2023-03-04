# To run the website from the command line, create the Environment Variables
# 1) Navigate to the folder
# 2) export FLASK_APP=main.py (linux, mac) // set FLASK_APP=main.py (windows)
# 3) Can now type 'flask run' // 'python -m flask run'
# www.localhost:5000
# 4) Additionally; export FLASK_APP=1 // set FLASK_DEBUG=1

# Flask is the root for a flask instance
# render_template searches project directory for 'templates' folder
# url_for provides references to personalised folder-names

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flaskblog.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'      # Same as url_for, reference the function name
login_manager.login_message = "Login required to access Account page"
login_manager.login_message_category = 'info'   # Reference to bootstrap style



def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    # This is an additional requirement that creates a specific folder for the database
    app.app_context().push()

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)

    return app
