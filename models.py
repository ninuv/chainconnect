from app import db, app
from flask_login import UserMixin, LoginManager
from datetime import datetime, timezone

# Table relationship
post_likes = db.Table(
    'post_likes',
    db.Column('user_id', db.String(200), db.ForeignKey('users.id'), primary_key=True),
    db.Column('post_id', db.String(200), db.ForeignKey('posts.id'), primary_key=True)
)
follows = db.Table(
    'follows',
    db.Column('follower_id', db.String(200), db.ForeignKey('users.id'), primary_key=True),
    db.Column('followed_id', db.String(200), db.ForeignKey('users.id'), primary_key=True)
)
blocklist = db.Table(
    'blocklist',
    db.Column('blocker_id', db.String(200), db.ForeignKey('users.id'), primary_key=True),
    db.Column('blocked_id', db.String(200), db.ForeignKey('users.id'), primary_key=True)
)

# models
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.String(200), primary_key=True)
    fullname = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.Integer, default=1)                                     # role = 0: suspended user, role = 1: regular user, role = 2: admin, role = 3: overseer, role = 4: account moderator, role = 5: content moderator,
    bio = db.Column(db.Text, nullable=True)
    pronouns = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    app_lang = db.Column(db.String(5), default='deu') # eng, deu, swe, ser

    likes_total = db.Column(db.Integer, default=0)

    posts = db.relationship('Post', backref='author', lazy='dynamic', cascade='all')
    comments = db.relationship('Comment', backref='author', lazy='dynamic', cascade='all')
    toggled_notifications = db.relationship('Notification', backref='toggler', lazy='dynamic')
    toggled_protocols = db.relationship('Protocol', backref='toggler', lazy='dynamic')
    liked_posts = db.relationship('Post', secondary=post_likes, back_populates='liked_by', lazy='dynamic')
    following = db.relationship('User', secondary=follows, primaryjoin=(follows.c.follower_id == id), secondaryjoin=(follows.c.followed_id == id), backref=db.backref('followed_by', lazy='dynamic'), lazy='dynamic')
    blocked_users = db.relationship('User', secondary=blocklist, primaryjoin=(blocklist.c.blocker_id == id), secondaryjoin=(blocklist.c.blocked_id == id), backref=db.backref('blocked_by', lazy='dynamic'), lazy='dynamic')



class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.String(200), primary_key=True)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    user_id = db.Column(db.String(200), db.ForeignKey('users.id'), nullable=False)

    liked_by = db.relationship('User', secondary=post_likes, back_populates='liked_posts', lazy='dynamic')
    like_count = db.Column(db.Integer, default=0)
    comments = db.relationship('Comment', backref='original_post', lazy='dynamic', cascade='all')



class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.String(200), primary_key=True)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    user_id = db.Column(db.String(200), db.ForeignKey('users.id'), nullable=False)
    original_post_id = db.Column(db.String(200), db.ForeignKey('posts.id'), nullable=False)

    parent_id = db.Column(db.String(200), db.ForeignKey('comments.id'), nullable=True) # not used when the Post is its direct parent
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]), lazy='dynamic', cascade='all, delete-orphan')



class Protocol(db.Model):                               # functions: Register, Log in, Log out, Delete account, Change username
    id = db.Column(db.String(200), primary_key=True)
    event_id = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.String(10), db.ForeignKey('users.id'), nullable=False)
    user_name = db.Column(db.String(200), nullable=False)


class Notification(db.Model):                           # functions: Like, Comment, Follow
    id = db.Column(db.String(200), primary_key=True)
    event_id = db.Column(db.String(10), nullable=False)
    receiving_user_id = db.Column(db.String(200), nullable=False)
    toggle_user_id = db.Column(db.String(200), db.ForeignKey('users.id'), nullable=False)
    comment_id = db.Column(db.String(200), nullable=True) # optional
    post_id = db.Column(db.String(200), nullable=True) # optional


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(str(user_id))

with app.app_context():
    #user1 = User(id='UM-287431', name='Tom', password='555creeper', email='t@tom.de', role='R-100001')
    #user2 = User(id='UM-927153', name='Ninu', password='555creeper', email='v_ninu@gmx.de', role='R-100002')
    #db.session.add(user1)
    #db.session.add(user2)
    #db.session.commit()
    db.create_all()