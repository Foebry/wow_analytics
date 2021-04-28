"""main program functionality"""
from functions import *
from datetime import datetime

import concurrent.futures
import os
import argparse



def setup(test):
    from databases.Database import Database
    from logger.Logger import Logger
    from realms import Realm
    from config import REALMS, DATABASE, DATABASE_TEST

    logger = Logger(os.getcwd(), "d")

    logger.log(msg="\n"*3, timestamped=False, level_display=False)
    logger.log(msg="*"*150, timestamped=False, level_display=False)
    logger.log(msg="*"*65+"Started new session!"+"*"*65, timestamped=False, level_display=False)
    logger.log(msg="*"*150, timestamped=False, level_display=False)

    realms = [Realm(_id, REALMS[_id]) for _id in REALMS]

    if test:
        db = Database(DATABASE_TEST, logger)
        return logger, realms, db

    db = Database(DATABASE, logger)
    return logger, realms, db



def wait(duration):
    import time
    end = time.time() + duration

    while not time.time() >= end:
        remaining = round(end - time.time())

        print(" "*100, end="\r")
        print("sleeping {} seconds".format(remaining), end='\r')
        time.sleep(1)



def init(realm, live_data=None, start=False):
    from functions import setLiveData
    from Requests import Request
    from config import CREDENTIALS
    if start:
        request = Request(CREDENTIALS, logger)
        live_data = setLiveData(realm.id, db, logger, request)
        temp = live_data["auctions"][realm.id].copy()
        previous_auctions = {realm.id:temp}
        previous_response = {}
    else:
        temp = live_data["auctions"][realm.id].copy()
        previous_auctions = {realm.id:temp}
        request = None
        previous_response = None
    insert_data = {"auctions":{realm.id:[]}, "items":[], "classes":[], "subclasses":[], "pets":[], "mounts":[], "item_prices":[]}
    update_data = {}

    return live_data, insert_data, update_data, previous_auctions, request, previous_response




def main(realm):
    live_data, insert_data, update_data, previous_auctions, request, previous_response = init(realm, start=True)

    while True:
        # make request
        response = request.getAuctionData(realm.id, logger)
        if not response == previous_response:
            logger.log(msg="\n\n"+"*"*100, timestamped=False, level_display=False)
            logger.log(msg=f"New data of {len(response)} auctions")
            previous_response = response

            # set auction data
            setAuctionData(realm.id, response, live_data, insert_data, update_data, previous_auctions, request, db, logger)

            # insert data & update data
            insertData(db, live_data, insert_data, update_data, previous_auctions, realm.id, logger)
            updateData(db, update_data, realm.id, logger)

            _, insert_data, update_data, previous_auctions, _, _ = init(realm, live_data)

        # wait
        wait(600)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", dest="test", action="store_true")
    args = parser.parse_args()
    logger, realms, db = setup(args.test)

    for realm in realms:
        main(realm)
