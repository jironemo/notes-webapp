
from flask import Blueprint,render_template,request,flash,redirect,url_for

from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import login_user,logout_user,current_user,login_required

auth = Blueprint('auth', __name__)


@auth.route('/login',methods=['GET', 'POST'])
def login():
    from .models import User
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if(user is None):
            flash('Invalid email or password','error')
            return redirect(url_for('auth.login'))
        elif(check_password_hash(User.query.filter_by(email=email).first().password,password)):
            flash("Login Successful",'success')
            login_user(user,remember=False)
            return redirect(url_for('views.home'))
        else:
            flash('Invalid email or password','error')
    return(render_template('login.html',user=current_user))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up',methods=['GET', 'POST'])
def sign_up():
    from .models import User
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password = request.form.get('password')
        confirmPassword = request.form.get('confirmPassword')
        if(len(email) < 4):
            flash("Email too short",category='error')
        elif(len(firstName) < 2):
            flash("username too short",category='error')
        elif(password != confirmPassword):
            flash("passwords don't match",category='error')
        elif(len(password) < 7):
            flash("password too short",category='error')
        else:
            #add user to db
            new_user = User(email=email,firstName=firstName,password=generate_password_hash(password,method = 'sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("account created!",category='success')
            print(email+" "+password)
            login_user(new_user,remember=True)
            return redirect(url_for('views.home'))
            

    return render_template('signup.html',user=current_user)