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

        if kwargs:
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
        else:
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
        """Updating live_data, update_data dictionaries and possibly insert_data"""
        # calculate sold_quantity, new buyout of sold_quantity and bid of sold_quantity
        sold_quantity = existing.quantity - self.quantity
        buyout = existing.unit_price * sold_quantity
        bid = existing.bid * sold_quantity

        set_realm_update_data_auctions = "auctions" in update_data and self.realm_id in update_data["auctions"]
        unset_realm_update_data_auctions = "auctions" in update_data and self.realm_id not in update_data["auctions"]
        unset_auctions_update_data = "auctions" not in update_data

        # new time_posted = existing time_posted
        self.time_posted = existing.time_posted
        self.last_updated = setTimePosted(posted=self.time_posted)

        if sold_quantity > 0:
            # create sold_auction
            args = (self, self.realm_id, self.id, existing.item_id, self.pet_id, sold_quantity, self.unit_price, self.time_left, bid, buyout, self.time_posted, True)
            sold_auction = SoldAuction(insert_data, update_data, logger, *args)

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
    def __init__(self, insert_data, update_data, logger, *args):
        """Constructor for sold auctions. Takes in 1 argument:
            :arg *args: list"""

        self.auction = args[0]
        self.id = args[2]
        self.realm_id = args[1]
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
        self.insert(insert_data, update_data, logger)


    def insert(self, insert_data, update_data, logger):
        """updates sold_data. Takes in 2 arguments:
            :arg insert_data: dict
            :arg update_data: dict"""


        item = self.auction.Item
        try:item.sold += self.quantity
        except: return
        item.price += self.quantity * self.unit_price
        temp_mean = item.price / self.quantity
        new_mean = not temp_mean == item.mean_price
        valid = self.time_left != "SHORT" and self.unit_price < 9999999.9999 and self.unit_price < 5*item.mean_price
        sold = self.partial or valid

        partial_set_realm_insert_data_sold_auctions = self.partial and "sold_auctions" in insert_data and self.realm_id in insert_data["sold_auctions"]
        partial_unset_realm_insert_data_sold_auctions = self.partial and "sold_auctions" in insert_data and self.realm_id not in insert_data["sold_auctions"]
        partial_unset_sold_auctions_insert_data = self.partial and "sold_auctions" not in insert_data

        valid_complete_set_realm_insert_data_sold_auctions = not self.partial and valid and "sold_auctions" in insert_data and self.realm_id in insert_data["sold_auctions"]
        valid_complete_unset_realm_insert_data_sold_auctions = not self.partial and valid and "sold_auctions" in insert_data and self.realm_id not in insert_data["sold_auctions"]
        valid_complete_unset_sold_auctions_insert_data = not self.partial and valid and "sold_auctions" not in insert_data


        if partial_set_realm_insert_data_sold_auctions or valid_complete_set_realm_insert_data_sold_auctions:
            insert_data["sold_auctions"][self.realm_id].append(self)
            item.mean_price = temp_mean

        elif partial_unset_realm_insert_data_sold_auctions or valid_complete_unset_realm_insert_data_sold_auctions:
            insert_data["sold_auctions"][self.realm_id] = [self]
            item.mean_price = temp_mean

        elif partial_unset_sold_auctions_insert_data or valid_complete_unset_sold_auctions_insert_data:
            insert_data["sold_auctions"] = {}
            insert_data["sold_auctions"][self.realm_id] = [self]
            item.mean_price = temp_mean

        if sold and new_mean:
            item.update(update_data, insert_data, logger)
