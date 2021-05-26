from wtforms import Form
from wtforms import StringField,TextField,IntegerField
from wtforms.fields.html5 import EmailField
from wtforms import validators

class CommentForm(Form):
    username = StringField('username',
                [
                    validators.length(min=4, max=25, message='Insert a valid username'),
                    validators.Required(message='Username is Required')
                ])
    email = EmailField('email',
                [
                    validators.Required(message='The email is required'),
                    validators.Email(message='Insert a valid email')
                ])
    total = IntegerField('total')