from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, HiddenField, SelectField

class AddToCart(FlaskForm):
    quantity = IntegerField('Quantity')
    id = HiddenField('ID')

class Checkout(FlaskForm):
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    phone_number = StringField('Number')
    email = StringField('Email')
    pick_up_time = SelectField('Country', choices=[
                          ('ASAP', 'ASAP'), ('Within 1hr', ' Within 1hr'), ('Tomorrow', 'Tomorrow')])
    card_number = StringField('Card Number')
    card_exp = StringField('Card Expiration')
    card_secure_code = StringField('Card Security Code')
    payment_type = SelectField('Payment Type', choices=[
                                ('CASH', 'CASH'),('VISA', 'VISA'), ('MASTER', 'MASTER'), ('AMEX', 'AMEX')])

