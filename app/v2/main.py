from unittest import result
from flask import Blueprint, render_template, request, session, flash, redirect, url_for
import mysql

main2 = Blueprint("main2", __name__)

@main2.route("/")
def index_safe():
    if 'user' not in session: 
        flash("login to access this page", "danger")
        return redirect(url_for("auth2.login"))

    result = get_all_comments()
    return render_template("index-safe.html", result=result)

@main2.route("/search")
def search():
    return render_template("post/search.html")

@main2.route("/query")
def query():
    q = request.args.get("q")
    result = search_comment(q)

    return result

def get_all_comments():
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="shyam1947",
            database="work"
        )

        cur = db.cursor(dictionary=True)

        select_query = "SELECT * FROM comments"

        cur.execute(select_query)
        result = cur.fetchall()
        
        cur.close()
        db.close()

        return result

    except Exception as e:
        print(str(e))
        return False

def search_comment(query):
    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="shyam1947",
            database="work"
        )

        cur = db.cursor(dictionary=True)

        select_query = "SELECT title, comment, username, created_at FROM comments WHERE title LIKE '%" + query + "%' "
        print(select_query)

        cur.execute(select_query)
        result = cur.fetchall()
        
        cur.close()
        db.close()

        return result

    except Exception as e:
        print(str(e))
        return False
