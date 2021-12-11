from datetime import datetime

from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class CryptoCoins(db.Model):
    coin_id = db.Column(db.String(25), primary_key=True)
    coin_name = db.Column(db.String(30), index=True, unique=True)
    coin_symbol = db.Column(db.String(15), index=True, unique=True)
    coin_market_price = db.Column(db.Float(100), nullable=True)
    tag = db.relationship('Tags', backref='associated_tags', lazy='dynamic')

    def __repr__(self):
        return '<CryptoCoins {}, {}, {}>'.format(self.coin_id, self.coin_name, self.coin_symbol)


class Tags(db.Model):
    tag_id = db.Column(db.Integer, primary_key=True)
    coin_id = db.Column(db.String(25), db.ForeignKey('crypto_coins.coin_id'))
    coin_tag = db.Column(db.String(100), index=True)

    def __repr__(self):
        return '<Tags {} : {}>'.format(self.coin_tag, self.coin_id)