
##### FLASK SETUP #####
import os
from flask import Flask 
app = Flask(__name__)
app.secret_key = os.urandom(24)

##### IMPORTS #####
from flask import redirect, render_template,Response, request, url_for
from forms import RegisterForm, LoginForm
from sqlalchemy.ext.declarative import declarative_base
from model import Base, User

#### LOGIN IMPORTS ####
from flask_login import login_required, current_user,login_user, logout_user, LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

##### SQLAlchemy ####
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///database.db', connect_args= {'check_same_thread': False}, echo=True)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()



#### LOGIN #####

@login_manager.user_loader
def load_user(user_id):
    user = session.query(User).filter_by(id=user_id)
    if user.count() == 0:
    	return
    return user.first()

@app.route('/', methods=['GET', 'POST'])
def login(): 
	if request.method == 'GET':
		return render_template('login.html')

	email = request.form.get('email')
	pw = request.form.get('pw')
	user = session.query(User).filter_by(email=email) 

	if user.count() == 1:
		user = user.first()
		if user.check_password(pw):
			login_user(user)
			return redirect('/home')
		return 'Wrong Password'
	return 'Wrong Email'

@app.route('/signup', methods=['GET','POST'])
def sign_up():
	if request.method == 'GET':
		return render_template('sign_up.html')

	else:

		new_name     = request.form.get('name')
		new_email    = request.form.get('email')
		new_pw       = request.form.get('pw')

		u = User(email=new_email,name=new_name,pw_hash=new_pw)
		u.set_password(new_pw)
		session.add(u)
		session.commit()
		return redirect('/')

@app.route('/logout')
def logout():
	logout_user()
	return redirect('/')



	#### ROUTES ###
@app.route('/home')
@login_required
def home():
	return render_template('home.html', current_user = current_user)


if __name__=='__main__':
	app.run(debug=True)


