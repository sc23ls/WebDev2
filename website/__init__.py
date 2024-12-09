from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from os import path
from flask_login import LoginManager
from flask import Flask,request, session
from flask_admin import Admin
from flask_babel import Babel

def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'en')


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

babel = Babel(app, locale_selector=get_locale)
admin = Admin(app, template_mode='bootstrap4')

migrate = Migrate(app, db)

from .models import User

login_manager= LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader 
def load_user(id): 
    return User.query.get(int(id)) 


from website import views, models, auth