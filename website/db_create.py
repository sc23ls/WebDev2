from config import SQLALCHEMY_DATABASE_URI
from website import db
import os.path

# creating database
db.create_all()