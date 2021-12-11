from app import db
from app.models import User, Post, CryptoCoins


def db_test():

    u = User(username='sandy', email='sandy@example.com')
    # db.session.add(u)
    # db.session.commit()

    # u = User.query.all()
    # p = Post.query.all()
    # print(u)
    # print(p)

    # u = User.query.get(2)
    # p = Post(body='2my first post!', author=u)
    # db.session.add(p)
    # db.session.commit()

    # print("__" * 50)
    # users = User.query.all()
    # print("__" * 50)
    # print(users)
    # print("__" * 50)
    # for u in users:
    #     print(u.id, u.username)
    # print("+" * 50)
    # u = User.query.get(3)
    # print(u.id, u.username)
    # print("+" * 50)
    # print("1=" * 50)
    # print("Printing all posts written by a user.")
    # u = User.query.get(1)
    # posts = u.posts.all()
    # print(posts)
    #
    # print(">>" * 50)
    # for post in posts:
    #     print(post.id, post.author.username, post.body)
    # print(">>" * 50)
    #
    # print(">>" * 50)
    # u = User.query.get(2)
    # posts = u.posts.all()
    # for post in posts:
    #     print(post.id, post.author.username, post.body)
    # print(">>" * 50)
    #
    # users = User.query.all()
    # for u in users:
    #     db.session.delete(u)
    # posts = Post.query.all()

    # for p in posts:
    #     db.session.delete(p)
    # db.session.commit()


def insert_into_crypto_coins_table(coin_id, coin_name, coin_symbol):
    # creating CryptoCoins object from data provided and inserting into crypto_coins table.
    crypto_coins = CryptoCoins(coin_id=coin_id, coin_name=coin_name, coin_symbol=coin_symbol)
    # db.session.add(crypto_coins)
    # db.session.commit()

    # crypto_coins = CryptoCoins.query.all()
    print(crypto_coins)
    print(crypto_coins.coin_id)
    print(crypto_coins.coin_name)
    print(crypto_coins.coin_symbol)
