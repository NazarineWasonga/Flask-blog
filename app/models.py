from . import db, login_manager
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from time import time
from app import create_app

@login_manager.user_loader
def load_user(id):
        return User.query.get(int(id))
        
class User(UserMixin, db.Model):
    '''
    UserMixin class that includes generic implementations
    that are appropriate for most user model classes
    '''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(130))
    profile_pic_path = db.Column(db.String())

    post = db.relationship('Post', backref='user', lazy="dynamic")
    comments = db.relationship('Comments', backref='user', lazy="dynamic")

    pass_secure  = db.Column(db.String(255))

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)
   
    def __repr__(self):
        return '{}'.format(self.username)
    
class Post(db.Model):
    '''
    Post class represent the posts posted by 
    users.
    ''' 

    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    comments = db.relationship('Comments', backref='user', lazy="dynamic")

    @classmethod
    def retrieve_posts(cls, id):
        posts = Post.filter_by(id=id).all()
        return posts


    def __repr__(self):
        return '{}'.format(self.body)


class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    details = db.Column(db.String(255))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))