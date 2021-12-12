from app import db
from app.models import User, Post, CryptoCoins, Tags


def insert_into_crypto_coins_table(coin_id, coin_name, coin_symbol):
    crypto_coins = CryptoCoins.query.all()
    for each_crypto_coins in crypto_coins:
        if coin_id == each_crypto_coins.coin_id:
            return False
    # creating CryptoCoins object from data provided and inserting into crypto_coins table.
    crypto_coins = CryptoCoins(coin_id=coin_id, coin_name=coin_name, coin_symbol=coin_symbol)
    db.session.add(crypto_coins)
    db.session.commit()
    # adding default tag for this coin into the tags table.
    if coin_id != coin_symbol:
        insert_into_tags_table(tag=coin_id, coin=crypto_coins)
        insert_into_tags_table(tag=coin_symbol, coin=crypto_coins)
    else:
        insert_into_tags_table(tag=coin_id, coin=crypto_coins)
    if coin_name != coin_id and coin_name != coin_symbol:
        insert_into_tags_table(tag=coin_name, coin=crypto_coins)
    # printing all the entry of the crypto_coins table for testing purpose
    crypto_coins = CryptoCoins.query.all()
    print(crypto_coins)
    for each_crypto_coins in crypto_coins:
        print(">>>>>>>>>>>>>>>>>>>>>>>")
        print(each_crypto_coins)
        print(each_crypto_coins.coin_id)
        # print(each_crypto_coins[1])
        # print(each_crypto_coins[2])
        print(">>>>>>>>>>>>>>>>>>>>>>>")
    return True


def get_data_from_crypto_currency():
    crypto_coins = CryptoCoins.query.all()
    return crypto_coins


def get_coin_id_list_from_db():
    all_data = get_data_from_crypto_currency()
    coin_ids_list = []
    for each_data in all_data:
        coin_ids_list.append(each_data.coin_id)
    return coin_ids_list


def get_coin_name_list_from_db():
    all_data = get_data_from_crypto_currency()
    coin_name_list = []
    for each_data in all_data:
        coin_name_list.append(each_data.coin_name)
    return coin_name_list


def insert_into_tags_table(tag, coin):
    tag_entry = Tags(associated_tags=coin, coin_tag=tag)
    db.session.add(tag_entry)
    db.session.commit()
    tag_lists = Tags.query.all()
    print(tag_lists)


