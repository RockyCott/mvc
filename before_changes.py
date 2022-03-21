from flask import Flask, request, make_response, redirect, render_template, session
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm


app = Flask(__name__)
Bootstrap = Bootstrap(app) #initializing boostrap instance - receives flask app

app.secret_key = 'testing'

class validate:
    user_ip = None
    def validate_ip():
    if user_ip is None:
        user_ip = request.remote_addr #getting ip from user with a request method
        session['user_ip'] = user_ip


@app.route('/')
def index():
    user_ip = request.remote_addr #getting ip from user with a request method
    response = make_response(redirect('/hello')) #redirecting the user to the main page
    session['user_ip'] = user_ip #addig user ip to the session foro storing in backend
    #response.set_cookie('user_ip', user_ip) #setting a cookie with the user's ip - this is stored in the client which is not secure

    return response
"""
@app.route('/login', methods=['GET', 'POST']) #get for showing login form, post for submitting login info
def login(user, pass):
    if request.method == 'POST':
        #get user and pass frrom database
        user = request.form['user']

        session['username'] = user 
        return redirect(url_for('start'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect(url_for('start'))
"""

@app.route('/hello')
def start():
    user_ip = session.get('user_ip') #getting user's ip from the brwser's cookies
    app.logger.info(f'new user with ip: {user_ip}')
    
    return render_template('main.html') 

@app.route('/ftw')
def freeThisWeek():
    return render_template('freeThisWeek.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('404_not_found.html', error = error)