"""auctions functionality"""
from datetime import datetime
from functions import setTimePosted, setTimeSold
from items import Item

import datetime
import random



class Auction():
    """docstring"""
    def __init__(self, live_data, logger, previous_auctions=None, insert_data=None, update_data=None, request=None, db=None, test=False, *args, **kwargs):
        """Auction constructor. Takes in 7 args. Always needs 6 arguments, so either args or kwargs need to be given:
            :arg live_data: dict,
            :arg previous_auctions: dict,
            :arg insert_data: dict,
            :arg update_data: dict,
            :arg sold_data: dict,
            :arg *args: list (optional),
            :arg **kwargs: dict (optional)"""

        rebuild_auction = insert_data is None and kwargs

        if rebuild_auction:
            self.id = kwargs["_id"]
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
            self.Item = kwargs["Item"]
            return

        self.realm_id = args[0]
        self.id = args[1]
        self.item_id = args[2]
        self.pet_id = args[3]["_id"]
        self.quantity = args[4]
        self.unit_price = args[5]
        self.time_left = args[6]
        self.bid = args[7]
        self.buyout = args[8]
        self.time_posted = setTimePosted(test=test)
        self.last_updated = self.time_posted

        first_pet = self.item_id == 82800 and self.item_id not in live_data["items"]
        is_pet = self.item_id == 82800 and self.item_id in live_data["items"]
        existing_pet = is_pet and self.pet_id in live_data["items"][self.item_id]
        new_pet = is_pet and self.pet_id not in live_data["items"][self.item_id]
        new_item = not self.item_id == 82800 and self.item_id not in live_data["items"]
        existing_item = not self.item_id == 82800 and self.item_id in live_data["items"]
        new_auction = insert_data is not None and self.id not in previous_auctions[self.realm_id]
        existing_auction = insert_data is not None and self.id in previous_auctions[self.realm_id]


        if existing_item:
            self.Item = live_data["items"][self.item_id]

        elif new_item:
            item = Item(logger, live_data, insert_data, update_data, request, self.item_id)
            live_data["items"][self.item_id] = item
            self.Item = item

        elif existing_pet:
            self.Item = live_data["items"][self.item_id][self.pet_id]

        elif new_pet:
            item = Item(logger, live_data, insert_data, update_data, request, self.item_id, args[3])
            live_data["items"][self.item_id][self.pet_id] = item
            self.Item = item

        elif first_pet:
            item = Item(logger, live_data, insert_data, update_data, request, self.item_id, args[3])
            live_data["items"][self.item_id] = {}
            live_data["items"][self.item_id][self.pet_id] = item
            self.Item = item

        else: return

        if new_auction:
            live_data["auctions"][self.realm_id][self.id] = self
            self.insert(insert_data, logger)

        elif existing_auction:
            self.update(live_data, previous_auctions, update_data, insert_data, live_data["auctions"][self.realm_id][self.id], logger)


    def insert(self, insert_data, logger):
        unset_insert_data_auctions = "auctions" not in insert_data
        unset_realm_insert_data_auctions = "auctions" in insert_data and self.realm_id not in insert_data["auctions"]
        set_realm_insert_data_auctions = "auctions" in insert_data and self.realm_id in insert_data["auctions"]

        if set_realm_insert_data_auctions:
            insert_data["auctions"][self.realm_id].append(self)

        elif unset_realm_insert_data_auctions:
            insert_data["auctions"][self.realm_id] = [self]

        elif unset_insert_data_auctions:
            insert_data["auctions"] ={}
            insert_data["auctions"][self.realm_id] = [self]


    def update(self, live_data, previous_auctions, update_data, insert_data, existing, logger):
        """
            Updating an Auction object.
            If auction is still active at t+1 we need to check if it is partially sold.
            Afterwards we remove the auction with equal id from t so the new one can take its place.
            If auction has fewer quantity, we know the auction got partially sold.
            We then create a Soldauction.
            Finally we add auction to update dictionary to be updated.
        """
        # calculate sold_quantity, new buyout of sold_quantity and bid of sold_quantity
        sold_quantity = existing.quantity - self.quantity
        buyout = existing.unit_price * sold_quantity
        bid = -1
        if existing.bid > -1: bid = existing.bid / existing.quantity * sold_quantity

        set_realm_update_data_auctions = "auctions" in update_data and self.realm_id in update_data["auctions"]
        unset_realm_update_data_auctions = "auctions" in update_data and self.realm_id not in update_data["auctions"]
        unset_auctions_update_data = "auctions" not in update_data

        # new time_posted = existing time_posted
        self.time_posted = existing.time_posted
        self.last_updated = setTimePosted(posted=self.time_posted)

        if sold_quantity > 0:
            # create sold_auction
            args = (existing, self.realm_id, self.id, self.item_id, self.pet_id, sold_quantity, self.unit_price, self.time_left, bid, buyout, self.time_posted, True)
            sold_auction = SoldAuction(live_data, insert_data, update_data, logger, *args)

        # remove auction_id from previous_auctions
        del previous_auctions[self.realm_id][self.id]

        # add to live_data
        live_data["auctions"][self.realm_id][self.id] = self

        # adding auction to be updated
        if set_realm_update_data_auctions:
            update_data["auctions"][self.realm_id].append(self)

        elif unset_realm_update_data_auctions:
            update_data["auctions"][self.realm_id] = [self]

        elif unset_auctions_update_data:
            update_data["auctions"] = {}
            update_data["auctions"][self.realm_id] = [self]



class SoldAuction():
    """docstring"""
    def __init__(self, live_data, insert_data, update_data, logger, *args):
        """Constructor for sold auctions. Takes in 1 argument:
            :arg *args: list"""

        self.auction = args[0]
        self.realm_id = args[1]
        self.id = args[2]
        self.item_id = args[3]
        self.pet_id = args[4]
        self.quantity = args[5]
        self.unit_price = args[6]
        self.time_left = args[7]
        self.bid = args[8]
        self.buyout = args[9]
        self.time_posted = args[10]
        self.time_sold = setTimeSold(posted=self.time_posted)
        self.partial = args[11]
        self.insert(live_data, insert_data, update_data, logger)


    def insert(self, live_data, insert_data, update_data, logger):
        """updates sold_data. Takes in 2 arguments:
            :arg insert_data: dict
            :arg update_data: dict"""

        from functions import isValidSoldAuction

        item = self.auction.Item

        set_sold_auctions_insert_data = "sold_auctions" in insert_data
        set_realm_insert_data_sold_auctions = set_sold_auctions_insert_data and self.realm_id in insert_data["sold_auctions"]


        if not set_sold_auctions_insert_data:
            insert_data["sold_auctions"] = {}
            insert_data["sold_auctions"][self.realm_id] = []

        elif not set_realm_insert_data_sold_auctions:
            insert_data["sold_auctions"][self.realm_id] = []

        if self.partial:
            # partially sold auctions will always be considered as sold
            insert_data["sold_auctions"][self.realm_id].append(self)
            return item.updateMean(self, update_data, insert_data, logger)

        auctions_to_check = [
                                insert_data["sold_auctions"][self.realm_id][x]
                                for x in range(len(insert_data["sold_auctions"][self.realm_id]))
                                if insert_data["sold_auctions"][self.realm_id][x].auction.Item.id == self.auction.Item.id
                        ]

        if isValidSoldAuction(live_data, self, auctions_to_check, logger):
            insert_data["sold_auctions"][self.realm_id].append(self)
            item.updateMean(self, update_data, insert_data, logger)
