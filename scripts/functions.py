"""extra functions not directly related to any class"""
import datetime
import random

def setTimePosted(posted=None, test=False):
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute_posted = 0
    second_posted = 0
    microsecond_posted = 0
    if posted:
        time_posted = datetime.datetime.strptime(posted, "%Y-%m-%d %H:%M:%S.%f")
        minute_posted = time_posted.minute
        second_posted = time_posted.second
        microsecond_posted = time_posted.microsecond
        minute = random.randrange(max(minute_posted, now.minute), 60)
        second = random.randrange(max(second_posted, now.second), 60)
        micro = random.randrange(max(microsecond_posted, now.microsecond), 1000000)
    elif test:
        hour = 12
        minute = 30
        second = 30
        micro = 500000
    else:
        minute = random.randrange(now.minute, 60)
        second = random.randrange(now.second, 60)
        micro = random.randrange(now.microsecond, 1000000)

    time_posted = datetime.datetime(year, month, day, hour, minute, second, micro)
    return time_posted.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


def setTimeSold(posted=None):
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    if posted: minute_posted = datetime.datetime.strptime(posted, "%Y-%m-%d %H:%M:%S.%f").minute
    else: minute_posted = 0
    minute = random.randrange(max(minute_posted, now.minute+1), 60)
    second = random.randrange(0, now.second + 1)
    micro = random.randrange(0, 1000000)

    time_sold = datetime.datetime(year, month, day, hour, minute, second, micro) - datetime.timedelta(hours=1)

    return time_sold.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]



def setAuctionData(realm_id, auction_data, live_data, insert_data, update_data, previous_auctions):
    """Setting auction data from getAuctionData response. Takes in 4 arguments:
      :arg realm_id: int,
      :arg auction_data: dict,
      :arg live_data: dict,
      :arg previous_auctions: dict"""
    from Wow_Analytics.scripts.auctions import Auction

    auctions = []
    for auction in auction_data:
        auction_id = auction["id"]
        item_id = auction["item"]["id"]
        if "pet_species_id" not in auction: pet = 0
        else: pet = {"id":auction["pet_species_id"], "quality_id":auction["pet_quality_id"], "level":auction["pet_level"], "breed_id":auction["pet_breed_id"]}
        quantity = auction["quantity"]
        time_left = auction["time_left"]
        time_posted = setTimePosted()
        last_updated = time_posted

        # all are given
        if "unit_price" in auction and "bid" in auction and "buyout" in auction:
            unit_price = auction["unit_price"]
            bid = auction["bid"]
            buyout = auction["buyout"]

        # bid is missing -> bid = -1
        elif "unit_price" in auction and "buyout" in auction and "bid" not in auctions:
            unit_price = auction["unit_price"]
            buyout = auction["buyout"]
            bid = -1

        # unit_price is missing -> unit_price = buyout / quantity
        elif "buyout" in auction and "bid" in auction and "unit_price" not in auction:
            buyout = auction["buyout"]
            bid = auction["bid"]
            unit_price = buyout / quantity

        # buyout is missing -> buyout = -1
        elif "unit_price" in auction and "bid" in auction and "buyout" not in auction:
            unit_price = auction["unit_price"]
            bid = auction["bid"]
            buyout = -1

        # buyout AND bid are missing -> buyout = unit_price*quantity, bid = -1
        elif "unit_price" in auction and "bid" not in auction and "buyout" not in auction:
            unit_price = auction["unit_price"]
            bid = -1
            buyout = unit_price * quantity

        # bid and unit_price are missing -> unit_price = buyout / quantity, bid = -1
        elif "buyout" in auction and "unit_price" not in auction and "bid" not in auction:
            buyout = auction["buyout"]
            unit_price = buyout / quantity
            bid = -1

        # buyout AND unit_price are missing -> buyout = -1, unit_price = bid / quantity
        elif "bid" in auction and "unit_price" not in auction and "buyout" not in auction:
            bid = auction["bid"]
            unit_price = bid / quantity
            buyout = -1

        args = (realm_id, auction_id, item_id, pet, quantity, unit_price, time_left, bid, buyout, time_posted, last_updated)
        auction = Auction(live_data, previous_auctions, insert_data, update_data, *args)
        # for testing purposes
        auctions.append(auction)
    # for testing purposes
    return auctions


def updateAuctions(database, update_data):
    """Updates all auctions in auctionhouses table with 1 update_query. Takes in 2 arguments:
        :arg database: obj<Database>,
        :arg update_data: dict"""

    update_query = "UPDATE auctionhouses \n"
    update_quantity = "SET\n    quantity = CASE auction_id \n"
    update_time_left = "    time_left = CASE auction_id \n"
    update_bid = "  bid = CASE auction_id \n"
    update_buyout = "   buyout = CASE auction_id \n"
    update_last_updated = " last_updated = CASE auction_id \n"
    where = "WHERE auction_id in ("

    for realm_id in update_data["auctions"]:
        for auction in update_data["auctions"][realm_id]:
            # completing partial update statements
            update_quantity += "     when %s then %s \n" %(auction.id, auction.quantity)
            update_time_left += "     when %s then %s \n" %(auction.id, f'"{auction.time_left}"')
            update_bid += "     when %s then %s \n" %(auction.id, auction.bid)
            update_buyout += "     when %s then %s \n" %(auction.id, auction.buyout)
            update_last_updated += "     when %s then %s \n" %(auction.id, f'"{auction.last_updated}"')
            where += "%s, "%auction.id
        # finishing partion update_statements
        update_quantity += "end,\n"
        update_time_left += "end,\n"
        update_bid += "end,\n"
        update_buyout += "end,\n"
        update_last_updated += "end\n"
        where = where[:-2]
        where += ");"
        # finishing complete statement
        update_query = update_query + update_quantity + update_time_left + update_bid + update_buyout + update_last_updated + where
        # executing update statement
        database.execute(update_query)



def insertAuctions(database, insert_data, previous_auctions):
    """Writes all sold auctions, both partially and fully sold auctions into database with 1 query. Takes in 3 arguments:
        :arg database: obj<Database>,
        :arg insert_data: dict,
        :arg previous_auctions: dict"""

    # inserting new auctions into auctionhouses
    for realm_id in insert_data["auctions"]:
        # creating and executing auctions_query
        if len(insert_data["auctions"][realm_id]) > 0:
            auctions_query = "INSERT into auctionhouses(realm_id, auction_id, item_id, pet_id, quantity, unit_price, time_left, bid, buyout, time_posted, last_updated) values\n"
            for auction in insert_data["auctions"][realm_id]:
                if auction.item_id == 82800: pet_id = auction.pet_id["id"]
                else: pet_id = 0
                auction_values = "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s),\n" %(realm_id, auction.id, auction.item_id, f"{pet_id}", auction.quantity, auction.unit_price, f'"{auction.time_left}"', auction.bid, auction.buyout, f'"{auction.time_posted}"', f'"{auction.last_updated}"')
                auctions_query += auction_values
            auctions_query = auctions_query[:-2] + ";"
            database.write(auctions_query)

    # adding fully sold auctions to insert_data
    for realm_id in previous_auctions:
        if len(previous_auctions[realm_id]) > 0:
            from Wow_Analytics.scripts.auctions import SoldAuction
            for auction_id in previous_auctions[realm_id]:
                auction = previous_auctions[realm_id][auction_id]
                args = (realm_id, auction.id, auction.item_id, auction.pet_id, auction.quantity, auction.unit_price, auction.time_left, auction.bid, auction.buyout, auction.time_posted, False)
                sold_auction = SoldAuction(insert_data, *args)

    # inserting new sold auctions into soldauctions
    for realm_id in insert_data["sold_auctions"]:
        if len(insert_data["sold_auctions"][realm_id]) > 0:
            sold_auctions_query = "INSERT into soldauctions(realm_id, auction_id, item_id, pet_id, quantity, unit_price, time_left, bid, buyout, time_sold, partial) values\n"
            for auction in insert_data["sold_auctions"][realm_id]:
                if auction.item_id == 82800: pet_id = auction.pet_id["id"]
                else: pet_id = 0
                auction_values = "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s),\n" %(realm_id, auction.id, auction.item_id, pet_id, auction.quantity, auction.unit_price, f'"{auction.time_left}"', auction.bid, auction.buyout, f'"{auction.time_sold}"', auction.partial)
                sold_auctions_query += auction_values
            sold_auctions_query = sold_auctions_query[:-2] + ";"
            database.write(sold_auctions_query)
