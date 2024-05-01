from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from dotenv import dotenv_values
from models import CommentModel
import jwt

main = Blueprint('main', __name__)

secrets = dotenv_values(".env")

@main.route("/")
def index(current_user=None):

    # print('cookie : ', request.cookies.get('access-token'))
    # print('session : ', session.get("access-token"))
    
    if session.get("access-token") or request.cookies.get('access-token'):
        try:
            jwt_token = request.cookies.get('access-token') if request.cookies.get('access-token') != None else session.get("access-token")

            current_user = jwt.decode(
                jwt=jwt_token, 
                key=secrets["FLASK_SECRET_KEY"],
                algorithms=[ "HS256"]
            )

            session['user'] = current_user
            comments = CommentModel.query.all()
            
            return render_template('index.html', username=current_user.get("username"), comments=comments)
        
        except Exception as e:
            return "error : " + str(e)
        
    else:
        flash("login to access this page", "danger")
        return redirect(url_for("auth.login"))
    

@main.route("/all-users")
def protect():
    if 'user' not in session: 
        flash("login to access this page", "danger")
        return redirect(url_for("auth.login"))
    
    else:
        return "All User Details Coming soon........"
    


        