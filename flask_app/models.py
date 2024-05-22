from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from flask_app import db, login_manager

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True)
    email = db.Column(db.String, unique=True, index=True)
    password_hash = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    @property
    def password(self):
        raise AttributeError("読み取り不可")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_duplicate_email(self):
        return db.session.query(User).filter_by(email=self.email).first() is not None

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)

class Genre(db.Model):
    __tablename__ = "genre"
    Genid = db.Column(db.Integer, primary_key=True)
    Genname = db.Column(db.String)
    caption = db.Column(db.String)

class Sitedata(db.Model):
    __tablename__ = "sitedata"
    siteid = db.Column(db.Integer, primary_key=True)
    sitename = db.Column(db.String)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    content = db.Column(db.String)
    mainpic = db.Column(db.String)
    category = db.Column(db.Integer)
    cordinates = db.Column(db.String)

class Comment(db.Model):
    __tablename__ = "comment"
    poster = db.Column(db.String)
    siteid = db.Column(db.Integer)
    content = db.Column(db.String)

class PSicture(db.Model):
    __tablename__ = "picture"
    poster = db.Column(db.String)
    siteid = db.Column(db.Integer)
    content = db.Column(db.String)
    
