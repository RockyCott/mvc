from typing import Text
from flask.helpers import flash
from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, TextAreaField, FileField, HiddenField
from wtforms.validators import DataRequired, Email, Length, EqualTo


###
### the different forms used in the app
### all except the searchForm are using hidden_tag() when used in the templates
###

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=3, max=18)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8, max=20)])
    login = SubmitField('Login')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email(message='Invalid email'), Length(max=30)])
    username = StringField('username', validators=[DataRequired(), Length(min=3, max=18)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8, max=20)])
    register = SubmitField('Register')


class CommunityForm(FlaskForm):
    community_name = StringField('community name', validators=[DataRequired()])
    description = TextAreaField('Description')
    facebook = StringField('Facebook group')
    discord = StringField('Discord Server')
    picture = FileField('Community picture', validators=[DataRequired()])
    add_community = SubmitField('Add community')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    post = SubmitField('Post')

class CommentForm(FlaskForm):
    content = TextAreaField('Write a comment', validators=[DataRequired()])
    send = SubmitField('Comment')

class searchForm(FlaskForm):
    query = StringField(label=None, validators=[DataRequired()])
    send = SubmitField('Search communities')

class ResetRequestForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email(message='Invalid email'), Length(max=30)])
    send = SubmitField('send code')

class PasswordResetForm(FlaskForm):
    password = PasswordField('New password', validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField('Enter new password again', validators=[DataRequired(), Length(min=8, max=20), EqualTo('password', message='The passwords must match.')])
    reset = SubmitField('Reset password')

class SuggestionForm(FlaskForm):
    subject = StringField(validators=[DataRequired()])
    suggestion = TextAreaField(validators=[DataRequired()])
    send = SubmitField('Send suggestion')

class UpdatePostForm(FlaskForm):
    idPost = StringField('id')
    content = TextAreaField('Content', validators=[DataRequired()])
    send = SubmitField('Update')

class UpdateCommunityForm(FlaskForm):
    idCommunity = StringField('id')
    description = TextAreaField('Description', validators=[DataRequired()])
    facebook = StringField('Facebook group')
    discord = StringField('Discord Server')
    image = FileField('New picture')
    update = SubmitField('Update')

class UpdatePasswordForm(FlaskForm):
    current = PasswordField('Current password', validators=[DataRequired(), Length(min=8, max=20)])
    new_password = PasswordField('New password', validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField('Enter new password again', validators=[DataRequired(), Length(min=8, max=20), EqualTo('new_password', message='The passwords must match.')])
    update = SubmitField('Update password')