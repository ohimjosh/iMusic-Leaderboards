from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5

followers = db.Table('followers',
                    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
                   )

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            
    def unfollow(self, user):
        if not self.is_following(user):
            self.followed.remove(user)
            
    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0
        
    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)
        
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
        

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return '<Post {}>'.format(self.body)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))




class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    track_name = db.Column(db.String(128))
    artist_name = db.Column(db.String(64))
    genre = db.Column(db.String(64))
    beats_per_minute = db.Column(db.Integer)
    song_data = db.relationship('SongData', backref='song')


    def __repr__(self):
        return '<Song: ID {}, track {}, artist {}, genre {}, bpm {}>'.format(self.id, self.track_name, self.artist_name, self.genre,
                self.beats_per_minute)



class SongData(db.Model):
    song_id = db.Column(db.Integer, db.ForeignKey('song.id'), primary_key=True)
    danceability = db.Column(db.Integer)
    loudness_dB = db.Column(db.Integer)
    valence = db.Column(db.Integer)
    acousticness = db.Column(db.Integer)
    speechiness = db.Column(db.Integer)


    def __repr__(self):
        return '<Song Data: {}, {}, {}, {}, {}, {}>'.format(self.song_id,
                                                            self.danceability,
                                                            self.loudness_dB,
                                                            self.valence,
                                                            self.acousticness,
                                                            self.speechiness)



