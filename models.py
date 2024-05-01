from werkzeug.security import check_password_hash, generate_password_hash
from extensions import db
from uuid import uuid4

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(), primary_key=True, default=str(uuid4()))
    role = db.Column(db.String(), default="USER")
    email = db.Column(db.String())
    username = db.Column(db.String())
    password = db.Column(db.String()) 
    comments = db.relationship("CommentModel", backref='users', cascade="all, delete")

    def __repr__(self):
        return f"<User {self.username}>"
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    @classmethod
    def check_user(cls, email):
        user = cls.query.filter_by(email=email).one_or_none()
        return user
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.remove(self)
        db.session.commit()

class  CommentModel(db.Model):
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text())
    user_id = db.Column(db.String(), db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime(), default=db.func.now())

    def __repr__(self) -> str:
        return f"<Comment {self.title}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

