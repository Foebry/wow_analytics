"""auctions functionality"""
from datetime import datetime
import datetime
import random



class Auction():
    """docstring"""
    def __init__(self, live_data, previous_auctions, insert_data, update_data, sold_data, *args, **kwargs):
        """docstring"""
        if kwargs:
            self.id = kwargs["id"]
            self.realm_id = kwargs["realm_id"]
            self.item_id = kwargs["item_id"]
            self.pet_id = kwargs["pet_id"]
            self.quantity = kwargs["quantity"]
            self.unit_price = kwargs["unit_price"]
            self.time_left = kwargs["time_left"]
            self.bid = kwargs["bid"]
            self.buyout = kwargs["buyout"]
            self.time_posted = kwargs["time_posted"]
            self.last_updated = kwargs["last_updated"]
        else:
            self.id = args[1]
            self.realm_id = args[0]
            self.item_id = args[2]
            self.pet_id = args[3]
            self.quantity = args[4]
            self.unit_price = args[5]
            self.time_left = args[6]
            self.bid = args[7]
            self.buyout = args[8]
            self.time_posted = args[9]
            self.last_updated = args[10]

        # If auction_id is not yet in live_auctions -> add it to live_auctions
        if not self.id in live_data["auctions"][1096]:
            live_data["auctions"][1096][self.id] = self

            # setting auction to be inserted
            insert_data["auctions"] = {}
            insert_data["auctions"][self.realm_id] = {}
            insert_data["auctions"][self.realm_id][self.id] = self
        # if auction_id is already in live_auctions -> update live_auctions
        else: self.Update(live_data, previous_auctions, update_data, insert_data, live_data["auctions"][self.realm_id][self.id], self)

    @staticmethod
    def update(live_data, previous_auctions, update_data, insert_data, existing, new):
        """docstring"""

        # calculate sold_quantity
        sold_quantity = existing.quantity - new.quantity
        time_left = new.time_left
        buyout = existing.unit_price * sold_quantity
        bid = existing.bid * sold_quantity
        time_sold = f"{datetime.datetime.now().date()} {datetime.datetime.now().hour-1}:{random.randrange(0,60)}:{random.randrange(0, 60)}.{random.randrange(0, 1000)}"

        # create and insert sold_auction
        args = (new.realm_id, new.id, new.item_id, new.pet_id, sold_quantity, new.unit_price, new.time_left, bid, buyout, time_sold, True)
        sold_auction = SoldAuction(*args)
        sold_auction.Insert(insert_data)

        # replace auction in live_data
        live_data["auctions"][new.realm_id][new.id] = new

        # adding auction to be updated
        if "auctions" in update_data:
            if new.realm_id in update_data["auctions"]:
                if new.id in update_data["auctions"][new.realm_id]: update_data["auctions"][new.realm_id][new.id] = new
                else: update_data["auctions"][new.realm_id][new.id] = new
            else:
                update_data["auctions"][new.realm_id] = {}
                update_data["auctions"][new.realm_id][new.id] = new
        else:
            update_data["auctions"] = {}
            update_data["auctions"][new.realm_id] = {}
            update_data["auctions"][new.realm_id][new.id] = new

        # checking if auction was in previous batch
        if new.id in previous_auctions: del previous_auctions[new.realm_id][new.id]



class SoldAuction():
    """docstring"""
    def __init__(self, *args):
        self.id = args[1]
        self.realm_id = args[0]
        self.item_id = args[2]
        self.pet_id = args[3]
        self.quantity = args[4]
        self.unit_price = args[5]
        self.time_left = args[6]
        self.bid = args[7]
        self.buyout = args[8]
        self.time_sold = args[9]
        self.partial = args[10]

    def insert(self, sold_data):
        """docstring"""
        if "sold_auctions" in insert_data:
            if self.realm_id in insert_data["sold_auctions"]:
                if self.id in sold_data["sold_auctions"][self.realm_id]: sold_data["sold_auctions"][self.realm_id][self.id].append(self)
                else: sold_data["sold_auctions"][self.realm_id][self.id] = [self]
            else:
                sold_data["sold_auctions"][self.realm_id] = {}
                sold_data["sold_auctions"][self.realm_id][self.id] = [self]
        else:
            sold_data["sold_auctions"] = {}
            sold_data["sold_auctions"][self.realm_id] = {}
            sold_data["sold_auctions"][self.realm_id][self.id] = [self]



def insertAuctions(database, insert_data, previous_auctions):
    """docstring"""

    # inserting new auctions to auctionhouses
    for realm_id in insert_data["auctions"]:
        # creating and executing auctions_query
        if len(insert_data["auctions"][realm_id]) > 0:
            auctions_query = "INSERT into auctionhouses(realm_id, auction_id, item_id, pet_id, quantity, unit_price, time_left, bid, buyout, time_posted, last_updated) values(\n"
            for auction in insert_data["auctions"][realm_id]:
                auction_values = "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s),\n" %(realm_id, auction.id, auction.item_id, auctions.pet_id, auctions.quantity, auction.unit_price, f"{auction.time_left}", auction.bid, auction.buyout, f"{auction.time_posted}", f"{auction.last_updated}")
                auctions_query += auction_values
            auctions_query = auctions_query[:-1] + ";"
            database.write(auctions_query)

    # inserting new partialy sold auctions to soldauctions
    for realm_id in insert_data["soldauctions"]:
        # creating and executing partialy sold sold_auctions_query
        if len(insert_data["sold_auctions"]) > 0:
            sold_auctions_query = "INSERT into soldauctions(realm_id, auction_id, item_id, pet_id, quantity, unit_price, time_left, bid, buyout, time_sold, partial) values(\n"
            for auction in insert_data["sold_auctions"][realm_id]:
                auction_values = "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s),\n" %(realm_id, auction.id, auction.item_id, auction.pet_id, auction.quantity, auction.unit_price, f"{auction.time_left}", auction.bid, auction.buyout, f"{auction.time_sold}", auction.partial)
                sold_auctions_query += auction_values
            sold_auctions_query = sold_auctions_query[:-1] + ";"
            database.write(sold_auctions_query)

    # inserting new completely sold auctions to soldauctions
    moderate_pricing = auction.unit_price < 9999999.9999 && auction.unit_price < 5*auction.Item.mean_price
    sold_auctions_query = "INSERT INTO soldauctions(realm_id, auction_id, item_id, pet_id, quantity, unit_price, time_left, bid, buyout, time_sold, partial) VALUES(\n"
    for realm_id in previous_auctions:
        # creating and executing fully sold sold_auctions_query
        for auction in previous_auctions[realm_id]:
            if auction.time_left != "SHORT" and moderate_pricing:
                auction_values = "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s),\n" %(realm_id, auction.id, auction.item_id, auction.pet_id, auction.quantity, auction.unit_price, f"{auction.time_left}", auction.bid, auction.buyout, f"{auction.time_sold}")
                sold_auctions_query += auction_values
            else: del previous_auctions[realm_id][auction.id]
        sold_auctions_query = sold_auctions_query[:-1] + ";"
        database.write(sold_auctions_query)



def updateAuctions(database, update_data):
    """docstring"""
    update_query = "UPDATE auctionhouses \n"
    update_quantity = "SET quantity = CASE auction_id \n"
    update_time_left = "SET time_left = CASE auction_id \n"
    update_bid = "set bid = CASE auction_id \n"
    update_buyout = "SET buyout = CASE auction_id \n"
    update_last_updated = "SET last_updated = CASE auction_id \n"

    for realm_id in update_data["auctions"]:
        for auction in update_data["auctions"][realm_id]:
            # completing partial update statements
            update_quantity += "     when %s then %s \n" %(auction.id, auction.quantity)
            update_time_left += "     when %s then %s \n" %(auction.id, f"{auction.time_left}")
            update_bid += "     when %s then %s \n" %(auction.id, auction.bid)
            update_buyout += "     when %s then %s \n" %(auction.id, auction.buyout)
            update_last_updated += "     when %s then %s \n" %(auction.id, f"{auction.last_updated}")
        # finishing partion update_statements
        update_quantity += "end,\n"
        update_time_left += "end,\n"
        update_bid += "end,\n"
        update_buyout += "end,\n"
        update_last_updated += "end;"
        # finishing complete statement
        update_query = update_query + update_quantity + update_time_left + update_bid + update_buyout + update_last_updated
        # executing update statement
        database.execute(update_query)


def setAuctionData(auction_data):
    """docstring"""
    pass
