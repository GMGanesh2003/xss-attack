from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_mysqldb import MySQL
from flask_wtf import CSRFProtect 

ckeditor = CKEditor()
mysql = MySQL()
csrf = CSRFProtect()
db = SQLAlchemy()
