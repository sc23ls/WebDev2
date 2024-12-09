from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

class editForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    shipping_address = StringField('shipping_address', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])