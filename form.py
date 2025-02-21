from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired ,length

    # flask_wtf ADd anime by search created Form 
class Add_Anime(FlaskForm):
    form_title = StringField('Title', validators=[DataRequired()],render_kw={"class": "semi-transparent-input"})
    Submit = SubmitField('ADD')
    
    #ADD Manga Page Form
class ADD_Manga(FlaskForm):
    Manga_title = StringField('Title', validators=[DataRequired()],render_kw={"class": "semi-transparent-input"})
    Submit = SubmitField('ADD')
    
    
    
class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign up')

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
