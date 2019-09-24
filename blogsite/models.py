from datetime import datetime
from blogsite import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Quotes:
    def __init__(self, id, author, quote, permalink):
        self.id=id
        self.author=author
        self.quote=quote
        self.permalink = permalink

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    image_file =  db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    blog = db.relationship('Blog', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)

    def __repr__(self):
         return f"user('{self.username}', '{self.email}', '{self.image_file}')"  

    

class Blog(db.Model):
    __tablename__ = "blogs"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='post', lazy=True)


    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"



class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    posted_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))

    
    def save_comment(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_comment(cls,id):
        comments = Comment.query.filter_by(post_id=id).all()
        return comments
    
    def __repr__(self):
        return f"Comment('{self.comment}', '{self.posted_date}')"
