from flask import Blueprint, redirect, render_template, request, session, url_for, flash
from dotenv import dotenv_values
from models import CommentModel
from forms import CommentForm
from extensions import db
import jwt

comments = Blueprint("comments", __name__)

secrets = dotenv_values(".env")

@comments.route("/add-comment", methods=['GET', 'POST'])
def add_comment():
    if session.get("access-token") or request.cookies.get("access-token"):
        form = CommentForm()
        try:
            jwt_token = request.cookies.get('access-token') if request.cookies.get('access-token') != None else session.get("access-token")

            current_user = jwt.decode(
                jwt=jwt_token, 
                key=secrets["FLASK_SECRET_KEY"],
                algorithms=[ "HS256"]
            )

            if form.validate_on_submit():
                title = form.title.data
                comment = form.comment.data
                user_id = session['user']['id']

                new_comment = CommentModel(
                    title = title,
                    body = comment,
                    user_id  = user_id
                )

                new_comment.save()

                return redirect(url_for("main.index"))
            
            return render_template("post/add_post.html", form=form)
        
        except Exception as e:
            return "error : " + str(e)
    
    else:
        return redirect("/login?next=/add-comment")

@comments.route("/delete-comment/<id>")
def delete_comment(id):
    if 'user' not in session:
        flash("Login to access this page", "danger")
        return redirect(url_for("main.index"))

    post_id = id
    comment = CommentModel.query.filter_by(id=post_id).first()
    if comment.users.id != session['user']['id']:
        return "<h1>403 : forbidden</h1> <br> Your are not owner of this comment to delete it"
    
    else:
        comment.delete()
        flash("Comment deleted successfully", "success")
        return redirect(url_for("main.index"))
