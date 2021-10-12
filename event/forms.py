#copied from class example.

from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField, DateTimeField, SelectField
from wtforms.fields.core import DateField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed

ALLOWED_FILE = {'PNG','JPG','png','jpg'}

#Create new event. flask form field types and other info at https://wtforms.readthedocs.io/en/2.3.x/fields/
class EventForm(FlaskForm):
  topic = SelectField('Topic', choices=[('bus', 'Business'), ('mh', 'Mental Health'), ('tech', 'Technology')])
  name = StringField('Event Name', validators=[InputRequired()])
  speaker = StringField('Speaker', validators=[InputRequired()])

  description = TextAreaField('Description', validators=[InputRequired()])
  date_time = DateTimeField('Date Time', validators=[InputRequired()], format = "%Y-%m-%d %H:%M'")
  address = StringField('Address', validators=[InputRequired()])
  image = FileField('Event Image', validators=[FileRequired(message='Image cannot be empty'), 
          FileAllowed(ALLOWED_FILE,message='Only supports png,jpg,PNG and JPG')])
  status = SelectField('Status', choices=[('green', 'Upcoming'), ('red', 'Cancelled'), ('grey', 'Inactive'), ('yellow', 'Booked')])
  submit = SubmitField("Create")
    
#User login
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

#User register
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    
    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    #submit button
    submit = SubmitField("Register")

#User comment
class CommentForm(FlaskForm):
  text = TextAreaField('Comment', [InputRequired()])
  submit = SubmitField('Create')