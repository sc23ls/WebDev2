import os

WTF_CSRF_ENABLED = True
SECRET_KEY = 'hfeufiowfjwijfcfjnf'

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True  

STRIPE_SECRET_KEY = 'sk_test_51QT2yXCF5WEueq3CFujYhzVMxaA5KbL5B2V8tmeZEJa1myy5IC17JsfdCRqwFewyY6UZBHxFUEJGIY33uoPaqsvT00wAwBl7SZ'