"""main program functionality"""
from auctions import Auction
from Requests import Request
from realms import Realm
from functions import *
from Wow_Analytics import config
from Databases.scripts.SQL import SQL
from Logger.Logger import Logger
from datetime import datetime

import concurrent.futures
import time





def init(realm, live_data=None, start=False):
    from Wow_Analytics.scripts.functions import setLiveData
    if start:
        request = Request(realm, logger)
        live_data = setLiveData(realm.id, db, logger, request)
        temp = live_data["auctions"][realm.id].copy()
        previous_auctions = {realm.id:temp}
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
    logger.log("\n"*3+"*"*25 + "Started new session" + "*"*25, timestamped=False)
    while True:

        # make request
        response = request.getAuctionData(realm.id, logger)
        if not response == previous_response:
            logger.log("\n\n"+"*"*100, timestamped=False)
            logger.log(f"New data of {len(response)} auctions")
            previous_response = response

            # set auction data
            setAuctionData(realm.id, response, live_data, insert_data, update_data, previous_auctions, request, db, logger)

            # insert data & update data
            insertData(db, insert_data, update_data, previous_auctions, realm.id, logger)
            updateData(db, update_data, realm.id, logger)
            init(realm, live_data)

        # wait
        print("sleeping", end='\r')
        time.sleep(600)


if __name__ == "__main__":
    realms = [Realm((name, config.REALMS[name])) for name in config.REALMS]
    db = SQL(config['DATABASE'])
    logger = Logger("E://Projects//Python//Wow_Analytics")

    for realm in realms:
        main(realm)
