from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path
db = SQLAlchemy()

DB_NAME = "database.db"
def create_app():
    app = Flask(__name__)
    UPLOAD_FOLDER = 'website\static\menu-upload'
    app.config['SECRET_KEY'] = 'dongbeimama123'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    db.init_app(app)
    from .views import views
    from .auth import auth
    from .admin import admin

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/')

    from .models import User, Note, Menu, MenuCategory

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    db.create_all(app=app)
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('created database!')

