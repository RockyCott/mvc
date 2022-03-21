from flask import Flask, request, make_response, redirect, render_template, session, flash
from flask.helpers import send_from_directory, url_for
from flask_wtf import form
from app.forms import LoginForm, SuggestionForm, UpdatePasswordForm

from app import create_app
from db_service import full_url, db_init, db
from models import User
from mail_service import mail
from flask_mail import Message
from flask_login import login_required, login_user, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from mail_service import mail_init
import random

ENV = 'dev'
app = create_app()
UPLOAD_FOLDER = 'app/static/community_pic'
TEMP_IMGS = 'app/static/temp_img'


if ENV=='dev':
    app.config['SQLALCHEMY_DATABASE_URI'] = full_url
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = f'''postgres://
jlsiyipjmdclno:5c8bbdc1721f023f039a0066f3f777207490b48b62045bcc
c78dbd59d6376d92@ec2-34-234-12-149.compute-1.amazonaws.com:5432/d2hsbdv3r00n9'''



app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TEMP_IMGS'] = TEMP_IMGS

db_init(app)
mail_init(app)

# for db tables creation

with app.app_context():
    db.create_all()



def validate_ip():
    if session.get('user_ip') is None:
        user_ip = request.remote_addr #getting ip from user with a request method
        session['user_ip'] = user_ip  #adding user ip to the session for storing in backend
        app.logger.info(f'new user with ip: {user_ip}')

 
@app.route('/')
@app.route('/start', methods = ['GET', 'POST'])
def start():
    validate_ip()
    user = current_user
    return render_template('main.html', current_user=user)

@app.route('/about')
def about():
    validate_ip()
    return render_template('about.html')

@app.route('/suggestions', methods=['GET', 'POST'])
@login_required
def suggestions():
    form = SuggestionForm()
    if form.validate_on_submit():
        suggestion = form.suggestion.data
        subject = form.subject.data
        sender = current_user.username    
        msg = Message(f'New suggestion: {subject}', recipients=['goodgamewebapp@gmail.com'])
        msg.body = f"""New suggestion by: {sender}

        {suggestion}
        """
        mail.send(msg)
        flash('Thank you, you have succesfully sent a new suggestion for this project!', 'info')
        return redirect(url_for('suggestions'))
    return render_template('suggest.html', form=form)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def getProfile():
    user = User.query.get_or_404(current_user.id)
    update_password = UpdatePasswordForm()
    if update_password.validate_on_submit():
        if check_password_hash(user.password, update_password.current.data):
            new_pass = update_password.new_password.data
            confirm_pass = update_password.confirm_password.data
            user.password = generate_password_hash(new_pass, method='pbkdf2:sha512')
            db.session.commit()
            flash('Your password has been updated!')
            return redirect(url_for('getProfile'))
        flash("The password you entered does not match with your current password", 'info')
    return render_template('profile.html', form = update_password)



@app.errorhandler(404)
def not_found(error):
    return render_template('404error.html', error = error)


@app.errorhandler(403)
def forbidden(error):
    return render_template('403error.html', error = error)


@app.errorhandler(410)
def gone(error):
    return render_template('410error.html', error = error)

@app.errorhandler(500)
def server_error(error):
    return render_template('500error.html', error = error)