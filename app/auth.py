from flask import Blueprint, flash, redirect, render_template, request, session, url_for, make_response
from forms import LoginForm, RegisterForm
from dotenv import dotenv_values
from datetime import timedelta
from models import UserModel
import jwt

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if session.get("access-token") is not None:
        return redirect(url_for("main.index"))
    

    secrets = dotenv_values(".env")
    form = LoginForm()
    next = request.args.get("next")

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = UserModel.check_user(email)
        
        if user is None or user.check_password(password) == False:
            flash("Invalid email or password", "danger")
            return redirect(url_for("auth.login"))
        
        else: 
            next = request.form.get("next")
            access_token = jwt.encode(
                payload={
                    "username" : user.username,
                    "email" : user.email,
                    "role" : user.role,
                    "id" : user.id
                }, 
                key=secrets['FLASK_SECRET_KEY'],
                algorithm="HS256"
            )   

            session['access-token'] = access_token 

            next_url = next if next else url_for("main.index")

            response = make_response(redirect(next_url))
            response.set_cookie('access-token', access_token, max_age=timedelta(hours=24))
            return response
    
    return render_template("auth/login.html", form = form, next=next)

@auth.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data

        user = UserModel.check_user(email)

        if user:
            flash("User email already in use", "danger")
            return redirect(url_for("auth.register"))
        
        else:
            new_user = UserModel(
                email=email,
                username = username
            )
            new_user.set_password(password)

            new_user.save()

            flash("Account created successfully", "success")
            return redirect(url_for("auth.login"))
    
    return render_template("auth/register.html", form = form)

@auth.route("/logout")
def logout():
    resp = make_response(redirect(url_for("auth.login")))

    session.pop('access-token', None)
    session.pop('user', None)

    if request.cookies.get('access-token'):
        resp.set_cookie('access-token', '', max_age=0)

    return resp
