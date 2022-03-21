from db_service import db
from datetime import datetime
from flask_login import UserMixin
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

from itsdangerous import TimedJSONWebSignatureSerializer as serializer
import string, secrets

class User(UserMixin, db.Model):
    __table_args__ = {'schema' : 'users_info'}
    id = db.Column(UUID(as_uuid=True), primary_key = True, default=uuid4)
    username = db.Column(db.String(50), unique = True, nullable = False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)
    date_registered = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    communities = db.relationship('Community', backref='creator')
    posts = db.relationship('Post', backref='postAuthor')
    comments = db.relationship('Comment', backref='author')

    def generate_token(self):
        expiration_sec = 3600
        s = serializer('secret', expiration_sec)
        token = s.dumps({'user_id': str(self.id)}).decode('utf-8')
        return token

    @staticmethod
    def validate_token(token):
        s = serializer('secret')
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

class Community(db.Model):
    __tablename__ = 'community'
    __table_args__ = {'schema' : 'communities'}
    id = db.Column(UUID(as_uuid=True), primary_key = True, default=uuid4)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(300))
    facebook = db.Column(db.String(250))
    discord = db.Column(db.String(250))
    picture = db.Column(db.Text, nullable=False)
    posts = db.relationship('Post', backref='communityPost')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    id_creator = db.Column(UUID(as_uuid=True), db.ForeignKey('users_info.user.id'))

class Post(db.Model):
    __tablename__ = 'post'
    __table_args__ = {'schema': 'communities'}
    id = db.Column(UUID(as_uuid=True), primary_key = True, default=uuid4)
    title = db.Column(db.String(60), nullable=False)
    content = db.Column(db.Text, nullable=False)
    community_id = db.Column(UUID(as_uuid=True), db.ForeignKey('communities.community.id'))
    comments = db.relationship('Comment', backref='from_post')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    id_author = db.Column(UUID(as_uuid=True), db.ForeignKey('users_info.user.id'))

class Comment(db.Model):
    __tablename__ = 'comment'
    __table_args__ = {'schema' : 'communities'}
    id = db.Column(UUID(as_uuid=True), primary_key = True, default=uuid4)
    content = db.Column(db.Text, nullable=False)
    post_id = db.Column(UUID(as_uuid=True), db.ForeignKey('communities.post.id'))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    id_author = db.Column(UUID(as_uuid=True), db.ForeignKey('users_info.user.id'))


#getting user for authentication or any other action
#didnt declare these functions in db_service to avoid overflow or some shit
#because then i needed to import them here for the UserModel and stuff
def get_user(username):
    return User.query.filter_by(username=username).first()

def get_by_email(email):
    return User.query.filter_by(email=email).first()

def user_by_id(id):
    return User.query.filter_by(id = id).first()


