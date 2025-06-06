from flask import java
from flask import Flask
from app.auth import auth
from app.main import main
from app.hack import hack
from app.v2.auth import auth2
from app.v2.main import main2
from app.v2.post import post2
from app.comments import comments
from extensions import db, csrf

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///db.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SECRET_KEY']="this-is-secret"


db.init_app(app)
csrf.init_app(app)  

app.register_blueprint(auth)
app.register_blueprint(main)
app.register_blueprint(hack)
app.register_blueprint(auth2, url_prefix="/v2")
app.register_blueprint(main2, url_prefix="/v2")
app.register_blueprint(post2, url_prefix="/v2")
app.register_blueprint(comments)
