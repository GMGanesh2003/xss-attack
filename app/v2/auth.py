from flask import Blueprint, render_template, flash, redirect, session, url_for
from forms import LoginForm, RegisterForm
import mysql.connector

auth2 = Blueprint('auth2', __name__)

@auth2.route("/login", methods=[ 'GET', 'POST' ])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        result = login_users(email, password)

        if result:
            session['user'] = result
            return redirect(url_for("main2.index_safe"))

        else:
            flash("Invalid email or password", "danger")
            return redirect(url_for("auth2.login"))

    return render_template("auth/login.html", form=form)

@auth2.route("/register", methods=[ 'GET', 'POST' ])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data

        result = create_user(email, username, password)

        if result:
            flash("user registration success", "success")
            return redirect(url_for("auth2.login"))

        else:
            flash("email already in use", "error")
            return redirect(url_for("auth2.register"))

    return render_template("auth/register.html", form=form)

@auth2.route("/logout")
def logout():
    session.pop('user', None)
    
    flash("Logout success", "success")
    return redirect(url_for("auth2.login"))

def create_user(email, username, password):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="shyam1947",
            database="work"
        )

        cur = db.cursor()
        insert_query = "INSERT INTO users(email, name, password) \
                        VALUES('" + email + "','" + username + "','" + password + "')"
        
        result = cur.execute(insert_query)
        db.commit()

        print(result)

        cur.close()
        db.close()
        
        return True

    except Exception as e:
        print(str(e))
        return False

def login_users(email, password):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="shyam1947",
            database="work"
        )

        cur = db.cursor(dictionary=True)

        select_query = "SELECT * FROM users WHERE email='" + email + "' AND password='" + password + "'"
        print(select_query)

        cur.execute(select_query)
        result = cur.fetchone()
        
        cur.close()
        db.close()

        return result

    except Exception as e:
        print(str(e))
        return False

@auth2.route("/test")
def test():
    email="' OR 1 = 1 -- "
    password = "wrong"

    result = login_users(email, password)  
    return str(result)