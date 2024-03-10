"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMG = "https://ociacc.com/wp-content/uploads/2019/03/blank-profile-picture-973460_1280-1030x1030.png"

def connect_db(app):
    app.app_context().push()
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User class"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True)
    first_name = db.Column(db.String(50),
                           nullable=False)
    last_name = db.Column(db.String(50),
                          nullable=False)
    image_url = db.Column(db.Text,
                          nullable=False,
                          default=DEFAULT_IMG)
    
    posts = db.relationship("Post", backref="user", cascade="all, delete")
    
class Post(db.Model):
    """model for blog posts"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.Text,
                      nullable=False)
    content = db.Column(db.Text,
                        nullable=False)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.datetime.now)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False,
                        passive_deletes=True)
    
