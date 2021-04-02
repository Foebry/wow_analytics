"""main program functionality"""
from Wow_Analytics.scripts.auctions import Auction
from Wow_Analytics.scripts.Requests import Request
from Wow_Analytics.scripts.realms import Realm
from Wow_Analytics.scripts.functions import *
from Databases.scripts.SQL import SQL
from Logger.Logger import *
from configparser import ConfigParser

import concurrent.futures
import time





def init(realm, live_data=None, start=False):
    from Wow_Analytics.scripts.functions import setLiveData
    if start:
        request = Request(realm, logger)
        live_data = setLiveData(realm.id, db, logger, request)
        temp = live_data["auctions"][realm.id].copy()
        previous_auctions = {realm.id:temp}
        print(previous_auctions)
        previous_response = {}
    else:
        temp = live_data["auctions"][realm.id].copy()
        previous_auctions = {realm.id:temp}
        request = None
        previous_response = None
    insert_data = {"auctions":{realm.id:[]}, "items":{}, "classes":[], "subclasses":[], "pets":[], "mounts":[]}
    update_data = {}

    return live_data, insert_data, update_data, previous_auctions, request, previous_response




def main(realm):
    live_data, insert_data, update_data, previous_auctions, request, previous_response = init(realm, start=True)
    while True:
        # make request
        response = request.getAuctionData(realm.id, logger)
        if not response == previous_response:
            print("new response")
            print(len(response))
            previous_response = response
            # set auction data
            setAuctionData(realm.id, response, live_data, insert_data, update_data, previous_auctions, request, db, logger)
            print("\nlive_items:", len(live_data["items"]))
            print("live_classes:", len(live_data["classes"]))
            # insert data & update data
            insertData(db, insert_data, update_data, previous_auctions, realm.id, logger)
            updateData(db, update_data, realm.id, logger)
            init(realm, live_data)
        # wait
        print("sleeping")
        time.sleep(600)


if __name__ == "__main__":
    config = ConfigParser()
    config.read('E:/Projects/Python/Wow_Analytics/config.ini')
    realms = [Realm(config, realm) for realm in config if realm not in ("DEFAULT", "DATABASE")]
    db = SQL(config['DATABASE'])
    logger = Logger("E://Projects//Python//Wow_Analytics")

    for realm in realms:
        main(realm)
        # except Exception: db.HandleError(db.connect(), Exception, None, logger)
        # except Exception as error: logger.log(type(err), error)
    # with concurrent.futures.ThreadPoolExecutor() as exe:
    #     [exe.submit(main, realm) for realm in realms]
