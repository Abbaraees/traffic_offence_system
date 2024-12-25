from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    
    if config_class:
        app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # Import and register blueprints here
    # from app.main import bp as main_bp
    # app.register_blueprint(main_bp)

    @app.route('/hello')
    def hello():
        return 'Hello World!'
    
    return app

from app import models