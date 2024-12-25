from flask import Flask, render_template
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
    from app.auth import auth as auth_bp
    app.register_blueprint(auth_bp)

    from app.main import main as main_bp
    app.register_blueprint(main_bp)

    from app.offences import offences as offences_bp
    app.register_blueprint(offences_bp)

    from app.offenders import offenders as offenders_bp
    app.register_blueprint(offenders_bp)


    @app.route('/hello')
    def hello():
        return 'Hello World!'
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app

from app import models