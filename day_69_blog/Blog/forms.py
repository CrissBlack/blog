from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired, URL, Email, Length
from flask_ckeditor import CKEditorField

class NewPostForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    subtitle = StringField('Subtitle', validators=[InputRequired()])
    img_url = StringField('Img address', validators=[URL()])
    # author = StringField('Author', validators=[InputRequired()])
    body = CKEditorField('Body', validators=[InputRequired()])
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    body = CKEditorField('Comment something', validators=[InputRequired()])
    submit = SubmitField('SUBMIT COMMENT')

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=3)])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Log In')