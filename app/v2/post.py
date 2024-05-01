from flask import Blueprint, render_template, session, flash, redirect, url_for
import mysql

from forms import CommentForm

post2 = Blueprint("post2", __name__)

@post2.route("/add-comment", methods=['GET', 'POST'])
def index_safe():
    if 'user' not in session: 
        flash("login to access this page", "danger")
        return redirect(url_for("auth.login"))
    
    form = CommentForm()

    if form.validate_on_submit():
        title = form.title.data
        comment = form.comment.data
        username = session['user']['name']

        insert_comment(title, comment, username)

        flash("comment added successfully", "success")
        return redirect(url_for("main2.index_safe"))


    return render_template("post/add_post.html", form=form)

def insert_comment(title, comment, username):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="shyam1947",
            database="work"
        )

        cur = db.cursor()

        insert_query = "INSERT INTO comments(title, comment, username) \
                        VALUES(%s, %s, %s)"

        result = cur.execute(insert_query, (title, comment, username, ))

        db.commit()

        cur.close()
        db.close()

        return result

    except Exception as e:
        print(str(e))
        return False
