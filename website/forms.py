from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, HiddenField, SelectField
class AddToCart(FlaskForm):
    quantity = IntegerField('Quantity')
    id = HiddenField('ID')
    
