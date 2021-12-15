from app import app
from app import db
from app.models import CryptoCoins, Tags


# method to perform insertion in DB table.
# returns true if data is valid and entered in to db and false otherwise.
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
        insert_into_tags_table(tag=coin_id, coin=coin_id)
        insert_into_tags_table(tag=coin_symbol, coin=coin_id)
    else:
        insert_into_tags_table(tag=coin_id, coin=coin_id)

    if coin_name != coin_id and coin_name != coin_symbol:
        insert_into_tags_table(tag=coin_name, coin=coin_id)

    # printing all the entry of the crypto_coins table for testing purpose
    crypto_coins = CryptoCoins.query.all()
    app.logger.debug(crypto_coins)
    for each_crypto_coins in crypto_coins:
        app.logger.debug(">>>>>>>>>>>>>>>>>>>>>>>")
        app.logger.debug(each_crypto_coins)
        app.logger.debug(each_crypto_coins.coin_id)
        app.logger.debug(">>>>>>>>>>>>>>>>>>>>>>>")
    return True


# method to get all data from crypto_coins table.
def get_data_from_crypto_currency():
    crypto_coins = CryptoCoins.query.all()
    return crypto_coins


# method to get coin_id of all the coin in the db.
def get_coin_id_list_from_db():
    all_data = get_data_from_crypto_currency()
    coin_ids_list = []
    for each_data in all_data:
        coin_ids_list.append(each_data.coin_id)
    return coin_ids_list


# method to get all coin's name from db.
def get_coin_name_list_from_db():
    all_data = get_data_from_crypto_currency()
    coin_name_list = []
    for each_data in all_data:
        coin_name_list.append(each_data.coin_name)
    return coin_name_list


# method to add new tag into db.
def insert_into_tags_table(tag, coin):
    tag = Tags(coin_id=coin, coin_tag=tag)
    db.session.add(tag)
    db.session.commit()

    tag_lists = Tags.query.all()
    app.logger.debug(tag_lists)


# method to add all the tags associated with a coin_id in the tags table of the db.
def get_tags_for_coin(coin_name):
    coin_id, coin_name, coin_symbol = get_coin_details(coin_name)
    app.logger.debug("coin_id = " + coin_id)

    coin_tag_details = Tags.query.filter_by(coin_id=coin_id).all()
    crypto_tag_list = []
    if len(coin_tag_details) != 0:
        for each in coin_tag_details:
            crypto_tag_list.append(each.coin_tag)

    return crypto_tag_list


# method to get all the details of any given coin from the db.
def get_coin_details(coin_name):
    coin_details = CryptoCoins.query.filter_by(coin_name=coin_name).first()
    return coin_details.coin_id, coin_details.coin_name, coin_details.coin_symbol


# tags associated with a given coin_id
def get_tags_for_coin_by_coin_id(coin_id):
    coin_tag_details = Tags.query.filter_by(coin_id=coin_id).all()
    crypto_tag_list = []
    for each in coin_tag_details:
        crypto_tag_list.append(each.coin_tag)
    return crypto_tag_list


# insert a new tag in db if it does not exist already in the db.
def process_insert_tag(coin_id, coin_tag):
    coin_all_tags = get_tags_for_coin_by_coin_id(coin_id)
    if coin_tag in coin_all_tags:
        return False
    else:
        insert_into_tags_table(coin_tag, coin_id)
        return True


# validate a tag if it exists in db or not.
def validate_tag_for_coin_id(coin_id, coin_tag):
    coin_all_tags = get_tags_for_coin_by_coin_id(coin_id)
    if coin_tag in coin_all_tags:
        return True
    else:
        return False


# delete a specific tag from the tag table if exist and return true otherwise return false.
def process_delete_tag(coin_id, coin_tag):
    coin_tags = get_tags_for_coin_by_coin_id(coin_id)
    if coin_tag in coin_tags:

        tag = Tags.query.filter_by(coin_id=coin_id, coin_tag=coin_tag).first()
        db.session.delete(tag)
        db.session.commit()
        return True
    else:
        return False


# delete coin with given coin id and all its associated tags.
def process_delete_coin(coin_id):
    coin_tags = get_tags_for_coin_by_coin_id(coin_id)
    for coin_tag in coin_tags:
        tag = Tags.query.filter_by(coin_id=coin_id, coin_tag=coin_tag).first()
        db.session.delete(tag)
        db.session.commit()
        app.logger.debug("one tag deleted")
    crypto_coins = CryptoCoins.query.filter_by(coin_id=coin_id).first()
    db.session.delete(crypto_coins)
    db.session.commit()
    app.logger.debug("one coin deleted.")




