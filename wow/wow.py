"""main program functionality"""
from datetime import datetime

import concurrent.futures
import os
import argparse



def setup(test):
    from databases.Database import Database
    from logger.Logger import Logger
    from realms import Realm
    from config import REALMS, DATABASE
    from operations import Operation
    from Requests import Request
    from config import CREDENTIALS

    logger = Logger(os.getcwd(), "d")

    logger.log(msg="\n"*3, timestamped=False, level_display=False)
    logger.log(msg="*"*150, timestamped=False, level_display=False)
    logger.log(msg="*"*65+"Started new session!"+"*"*65, timestamped=False, level_display=False)
    logger.log(msg="*"*150, timestamped=False, level_display=False)

    db = Database(DATABASE, logger, test)

    request = Request(CREDENTIALS, db, logger)

    operation = Operation(db, logger)
    operation.live_data = {"items":{82800:{}}, "classes":{}, "pets":{}, "mounts":{}}
    operation.insert_data = {"items":[], "classes":[], "subclasses":[], "pets":[], "mounts":[], "item_prices":[]}
    operation.update_data = {}

    for realm_id in REALMS:
        realm = Realm(realm_id, REALMS[realm_id], db, logger)
        operation.realms.append(realm)

    operation.setLiveData(request)

    return operation, request



def wait(duration):
    import time
    end = time.time() + duration

    while not time.time() >= end:
        remaining = round(end - time.time())

        print(" "*100, end="\r")
        print("sleeping {} seconds".format(remaining), end='\r')
        time.sleep(1)



def main():

    while True:
        round = True
        for realm in operation.realms:

            response = request.getAuctionData(realm, operation)

            if response:
                if round: operation.logger.log(msg="\n\n"+"*"*100, timestamped=False, level_display=False)
                operation.logger.log(msg=f"New data of {len(response)} auctions for {realm.name}")
                round = False

                realm.setAuctionData(response, operation, request)

                # realm.export(insert_data['items'])
        if len(operation.insert_data) > 0: operation.insertData()
        if len(operation.update_data) > 0: operation.updateData()

        operation.update()

        wait(600)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", dest="test", action="store_true")
    args = parser.parse_args()
    operation, request = setup(args.test)

    main()
