"""extra functions not directly related to any class"""
import datetime
import random
import concurrent.futures



class Operation:

    def __init__(self, db, logger):
        self.database = db
        self.logger = logger
        self.insert_data = {}
        self.update_data = {}
        self.live_data = {}
        self.realms = []



    def createInsertAuctionsQuery(self, section, realm):
        from math import floor

        print(" "*100, end="\r")
        print("inserting auctions {} - {}".format(section[0], section[1]), end="\r")

        begin = section[0]
        end = section[1]
        next = end + self.database.restraint
        remaining = end - begin
        auctions = len(self.insert_data["auctions"][realm.id])

        auctions_query = "INSERT into auctionhouses(realm_id, auction_id, item_id, pet_id, quantity, unit_price, time_left, bid, buyout, time_posted, last_updated) values\n"

        for auction in self.insert_data["auctions"][realm.id][begin:min(end, auctions)]:

            pet_id = 0
            if auction.item_id == 82800: pet_id = auction.pet_id

            auction_values = "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s),\n" %(realm.id, auction.id, auction.item_id, f"{pet_id}", auction.quantity, auction.unit_price, f'"{auction.time_left}"', auction.bid, auction.buyout, f'"{auction.time_posted}"', f'"{auction.last_updated}"')
            auctions_query += auction_values

        auctions_query = auctions_query[:-2] + ";"

        good_section = self.database.write(auctions_query)
        if not good_section: return self.createInsertAuctionsQuery((begin, floor(begin+remaining/2)), realm)

        if end < auctions: return self.createInsertAuctionsQuery((end, next), realm)

        return self.logger.log(msg=f"Inserted {auctions} auctions")



    def createUpdateAuctionsQuery(self, section, realm):
        from math import floor
        print(" "*100, end="\r")
        print("updating auctions {} - {}".format(section[0], section[1]), end="\r")

        begin = section[0]
        end = section[1]
        next = end +self.database.restraint
        remaining = end - begin
        auctions = len(self.update_data["auctions"][realm.id])

        update_query = "UPDATE auctionhouses \n"
        update_quantity = "SET\n    quantity = CASE auction_id \n"
        update_time_left = "    time_left = CASE auction_id \n"
        update_bid = "  bid = CASE auction_id \n"
        update_buyout = "   buyout = CASE auction_id \n"
        update_last_updated = " last_updated = CASE auction_id \n"
        where = "WHERE auction_id in ("
        realm_id = "\n  AND realm_id = {};".format(realm.id)

        for auction in self.update_data["auctions"][realm.id][begin:min(end, auctions)]:
            update_quantity += "    when {} then {} \n".format(auction.id, auction.quantity)
            update_time_left += "   when {} then {} \n".format(auction.id, f'"{auction.time_left}"')
            update_bid += " when {} then {} \n".format(auction.id, auction.bid)
            update_buyout += "  when {} then {} \n".format(auction.id, auction.buyout)
            update_last_updated += "    when {} then {} \n".format(auction.id, f'"{auction.last_updated}"')
            where += "{}, ".format(auction.id)

        update_quantity += "end,\n"
        update_time_left += "end,\n"
        update_bid += "end,\n"
        update_buyout += "end,\n"
        update_last_updated += "end\n"
        where = where[:-2]
        where += ")"

        update_query = update_query + update_quantity + update_time_left + update_bid + update_buyout + update_last_updated + where + realm_id

        good_section = self.database.update(update_query)
        if not good_section: return self.createUpdateAuctionsQuery((begin, floor(begin+remaining/2)), realm)

        if end < auctions: return self.createUpdateAuctionsQuery((end, next), realm)

        return self.logger.log(msg=f"Updated {auctions} auctions")



    def createSoldauctionsQuery(self, section, realm):
        from math import floor

        print(" "*100, end="\r")
        print("inserting soldauctions {} - {}".format(section[0], section[1]), end="\r")

        begin = section[0]
        end = section[1]
        next = end + self.database.restraint
        remaining = end - begin
        len_sold_auctions = len(self.insert_data["sold_auctions"][realm.id])


        sold_auctions_query = "INSERT into soldauctions(realm_id, auction_id, item_id, pet_id, quantity, unit_price, time_left, bid, buyout, time_sold, partial) values\n"

        for sold_auction in self.insert_data["sold_auctions"][realm.id][begin:min(end, len_sold_auctions)]:
            pet_id = 0
            if sold_auction.item_id == 82800: pet_id = sold_auction.pet_id

            auction_values = "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s),\n" %(realm.id, sold_auction.id, sold_auction.item_id, pet_id, sold_auction.quantity, sold_auction.unit_price, f'"{sold_auction.time_left}"', sold_auction.bid, sold_auction.buyout, f'"{sold_auction.time_sold}"', sold_auction.partial)
            sold_auctions_query += auction_values

        sold_auctions_query = sold_auctions_query[:-2] + ";"

        good_section = self.database.write(sold_auctions_query)
        if not good_section: return self.createSoldauctionsQuery((begin, floor(begin+remaining/2)), realm.id)

        if end < len_sold_auctions: return self.createSoldauctionsQuery((end, next), realm.id)

        return self.logger.log(msg=f"Inserted {len_sold_auctions} sold auctions")



    def createInsertItemsQuery(self, section):
        from math import floor

        print(" "*100, end="\r")
        print("inserting items {} - {}".format(section[0], section[1]), end="\r")

        begin = section[0]
        end = section[1]
        next = end + self.database.restraint
        remaining = end - begin
        items = len(self.insert_data["items"])

        insert_items_query = "INSERT INTO items(id, pet_id, mount_id, level, name, quality, class_id, subclass_id, type, subtype, mean_price) VALUES \n  "

        for index in range(len(self.insert_data["items"])):
            item = self.insert_data["items"][index]
            name = item.name
            # if " in name f-string "''" else f-string '""'
            if "'" in name and '"' in name:
                name = name.replace("'", "\'")
                name = name.replace('"', '\\"')
            elif "'" in name:
                name = name.replace("'", "\'")
            elif '"' in name:
                name = name.replace('"', '\\"')

            name = f'"{name}"'

            pet_id = item.pet_id
            mount_id = item.mount_id

            if pet_id is None: pet_id = 0
            if mount_id is None: mount_id = 0

            item_values = "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s),\n  "%(item.id, pet_id, mount_id, item.level, name, f'"{item.quality}"', item.class_id, item.subclass_id, f'"{item.type}"', f'"{item.subtype}"', item.mean_price)
            insert_items_query += item_values

        insert_items_query = insert_items_query[:-4] + ";"

        good_section = self.database.write(insert_items_query)
        if not good_section: return self.createInsertItemsQuery((start, floor(begin+remaining/2)))

        if end > items: return self.createInsertItemsQuery((end, next))

        return self.logger.log(msg=f"Inserted {items} items" )



    def createUpdateItemsQuery(self, section):
        from math import floor

        print(" "*100, end="\r")
        print("updateing items {} - {}".format(section[0], section[1]), end="\r")

        begin = section[0]
        end = section[1]
        next = end + self.database.restraint

        # if begin > end: RaiseError.ValueError("section[0] is greater then section[1] for createUpdateItemsQuery functions.py")

        remaining = end - begin
        items = len(self.update_data["items"])

        update_query = "UPDATE items \n SET mean_price = CASE \n"
        where = "where id in ("

        for item in self.update_data["items"][begin:min(end, items)]:
            update_query += "   when id = {} and pet_id = {} and mount_id = {} and level = {} then {}\n".format(item.id, item.pet_id, item.mount_id, item.level, item.mean_price)
            where += "{}, ".format(item.id)

        where = where[:-2] + ");"
        update_query += "   else mean_price \n end\n"
        update_query += where

        good_section = self.database.update(update_query)
        if not good_section: return self.createUpdateItemsQuery((begin, floor(begin+remaining/2)))

        if end < items: return self.createUpdateItemsQuery((end, next))

        return self.logger.log(msg=f"Updated {items} items")



    def createInsertMountsQuery(self, section):
        from math import floor

        print(" "*100, end="\r")
        print("inserting mounts {} - {}".format(section[0], section[1]), end="\r")

        begin = section[0]
        end = section[1]
        next = end + self.database.restraint

        remaining = end - begin
        mounts = len(self.insert_data["mounts"])

        insert_mounts_query = "INSERT INTO mounts(id, name, source, faction) VALUES \n  "

        for mount in self.insert_data["mounts"]:
            mount_values = "(%s, %s, %s, %s), \n    " %(mount.id, f'"{mount.name}"', f'"{mount.source}"', f'"{mount.faction}"')
            insert_mounts_query += mount_values

        insert_mounts_query = insert_mounts_query[:-7] + ";"

        good_section = self.database.write(insert_mounts_query)
        if not good_section: return self.createInsertMountsQuery((begin, floor(begin+remaining/2)))

        if end < mounts: return self.createInsertMountsQuery((end, next))

        return self.logger.log(msg=f"Inserted {mounts} mounts")



    def createInsertPetsQuery(self, section):
        from math import floor

        print(" "*100, end="\r")
        print("inserting pets {} - {}".format(section[0], section[1]), end="\r")

        begin = section[0]
        end = section[1]
        next = end + self.database.restraint

        remaining = end - begin
        pets = len(self.insert_data["pets"])

        insert_pets_query = "INSERT INTO pets(ID, name, type, source) VALUES \n "

        for pet in self.insert_data["pets"]:
            pet_values = "(%s, %s, %s, %s), \n  "%(pet.id, f'"{pet.name}"', f'"{pet.type}"', f'"{pet.source}"')
            insert_pets_query += pet_values

        insert_pets_query = insert_pets_query[:-5] + ";"

        good_section = self.database.write(insert_pets_query)
        if not good_section: return self.createInsertPetsQuery((begin, floor(begin+remaining/2)))

        if end < pets: return self.createInsertPetsQuery((end, next))

        return self.logger.log(msg=f"Inserted {pets} pets")



    def createInsertClassesQuery(self, section):
        from math import floor

        print(" "*100, end="\r")
        print("inserting classes {} - {}".format(section[0], section[1]), end="\r")

        begin = section[0]
        end = section[1]
        next = end + self.database.restraint

        remaining = end - begin
        classes = len(self.insert_data["classes"])

        insert_classes_query = "INSERT INTO classes(id, name) VALUES \n "

        for insert_class in self.insert_data["classes"]:
            class_values = "(%s, %s),\n "%(insert_class.id, f'"{insert_class.name}"')
            insert_classes_query += class_values

        insert_classes_query = insert_classes_query[:-3] + ";"

        good_section = self.database.write(insert_pets_query)
        if not good_section: return self.createInsertClassesQuery((begin, floor(begin+remaining/2)))

        if end < classes: return self.createInsertClassesQuery((end, next))

        return self.logger.log(msg=f"Inserted {classes} classes")



    def createInsertSubclassesQuery(self, section):
        from math import floor

        print(" "*100, end="\r")
        print("insertsubclasses {} - {}".format(section[0], section[1]), end="\r")

        begin = section[0]
        end = section[1]
        next = end + self.database.restraint

        remaining = end - begin
        subclasses = len(self.insert_data["subclasses"])


        insert_subclass_query = "INSERT INTO subclasses(Class_id, id, name) VALUES\n    "

        for subclass in self.insert_data["subclasses"]:
            subclass_values = "(%s, %s, %s),\n  "%(subclass.class_id, subclass.subclass_id, f'"{subclass.name}"')
            insert_subclass_query += subclass_values

        insert_subclass_query = insert_subclass_query[:-4] + ";"

        good_section = self.database.write(insert_subclass_query, logger)
        if not good_section: return self.createInsertSubclassesQuery((begin, floor(begin+remaining/2)))

        if end < subclasses: return self.createInsertSubclassesQuery((end, next))

        return self.logger.log(msg=f"Inserted {subclasses} subclasses")



    def updateData(self):
        """Updates all data to be updated (auctions, items). Takes in 2 arguments:
            :arg database: obj<Database>,
            :arg update_data: dict"""

        items_to_update = "items" in self.update_data and len(self.update_data["items"]) > 0
        realms_to_update = "realms" in self.update_data and len(self.update_data["realms"]) > 0

        self.logger.log(msg="\n")

        for realm in self.realms:
            auctions_to_update = "auctions" in self.update_data and len(self.update_data["auctions"][realm.id]) > 0
            if auctions_to_update:
                self.createUpdateAuctionsQuery((0, self.database.restraint), realm)

        if items_to_update:
            end = len(self.update_data["items"])
            self.createUpdateItemsQuery((0, self.database.restraint))

        if realms_to_update:
            for realm in self.update_data["realms"]: realm.update()



    def insertData(self):
        """
            Function responsible to write all data into the database.
        """
        items_to_insert = "items" in self.insert_data and len(self.insert_data["items"]) > 0
        item_prices_to_insert = "items" in self.update_data and len(self.update_data["items"]) > 0
        mounts_to_insert = "mounts" in self.insert_data and len(self.insert_data["mounts"]) > 0
        pets_to_insert = "pets" in self.insert_data and len(self.insert_data["pets"]) > 0
        classes_to_insert = "classes" in self.insert_data and len(self.insert_data["classes"]) > 0
        subclasses_to_insert = "subclasses" in self.insert_data and len(self.insert_data["subclasses"]) > 0

        self.logger.log(msg="\n")

        if mounts_to_insert:
            mounts = len(self.insert_data["mounts"])
            section = (0, min(self.database.restraint, mounts))
            self.createInsertMountsQuery(section)

        if pets_to_insert:
            pets = len(self.insert_data["pets"])
            section = (0, min(self.database.restraint, pets))
            self.createInsertPetsQuery(section)

        if classes_to_insert:
            classes = len(self.insert_data["classes"])
            section = (0, min(self.database.restraint, classes))
            self.createInsertClassesQuery(section)

        if subclasses_to_insert:
            subclasses = len(self.insert_data["subclasses"])
            section = (0, min(self.database.restraint, subclasses))
            self.createInsertSubclassesQuery(section)

        if items_to_insert:
            items = len(self.insert_data["items"])
            section = (0, min(self.database.restraint, items))
            self.createInsertItemsQuery(section)

        # insert prices
        if item_prices_to_insert:
            insert_string = "INSERT INTO item_prices (item_id, pet_id, time, value) VALUES \n "

            for index in range(len(self.update_data["items"])):
                item = self.update_data["items"][index]
                price_values = "(%s, %s, %s, %s), \n" %(item.id, item.pet_id, f'"{datetime.datetime.now() - datetime.timedelta(hours=1)}"', item.mean_price)
                insert_string += price_values

            insert_string = insert_string[:-3] + ";"
            self.database.write(insert_string)
            insert_strings = len(self.update_data["items"])
            self.logger.log(msg="Inserted %s item_price changes" %insert_strings)

        for realm in self.realms:
            auctions_to_insert = "auctions" in self.insert_data and realm.id in self.insert_data["auctions"] and len(self.insert_data["auctions"][realm.id]) > 0
            fully_sold_auctions = realm.id in realm.previous_auctions and len(realm.previous_auctions[realm.id]) > 0

            if auctions_to_insert:

                auctions = len(self.insert_data["auctions"][realm.id])
                section = (0, min(self.database.restraint, auctions))
                self.createInsertAuctionsQuery(section, realm)

            # adding fully sold auctions to insert_data
            if fully_sold_auctions:
                from auctions import SoldAuction
                for auction_id in realm.previous_auctions:
                    auction = realm.previous_auctions[auction_id]
                    args = (auction, auction.id, auction.item_id, auction.pet_id, auction.quantity, auction.unit_price, auction.time_left, auction.bid, auction.buyout, auction.time_posted, False)
                    sold_auction = SoldAuction(self.insert_data, self.update_data, self.logger, auction)

            sold_auctions_to_insert = "sold_auctions" in self.insert_data and len(self.insert_data["sold_auctions"][realm.id]) > 0

            if sold_auctions_to_insert:
                soldauctions = len(self.insert_data["sold_auctions"][realm.id])
                section = (0, min(self.database.restraint, soldauctions))
                self.createSoldauctionsQuery(section, realm)



    def setLiveMount(self, mount_data):
        from mounts import Mount

        _id = mount_data[0]
        name = mount_data[1]
        source = mount_data[2]
        faction = mount_data[3]

        kwargs = {"_id":_id, "name":name, "source":source, "faction":faction}

        self.live_data["mounts"][_id] = Mount(**kwargs)



    def setLivePets(self, pet_data):
        from pets import Pet

        _id = pet_data[0]
        name = pet_data [1]
        type = pet_data[2]
        source = pet_data[3]
        faction = pet_data[4]

        kwargs = {"_id":_id, "name": name, "type":type, "source":source, "faction":faction}

        self.live_data["pets"][_id] = Pet(**kwargs)


    def setLiveClasses(self, class_data):
        from classes import Class

        _id = class_data[0]
        name = class_data[1]

        kwargs = {"_id":_id, "name": name, "subclasses":{}}

        self.live_data["classes"][_id] = Class(**kwargs)


    def setLiveSubclasses(self, subclass_data):
        from classes import Subclass

        class_id = subclass_data[0]
        _id = subclass_data[1]
        name = subclass_data[2]

        kwargs = {"class_id":class_id, "subclass_id":_id, "name": name}

        self.live_data["classes"][class_id].subclasses[_id] = Subclass(**kwargs)


    def setLiveItem(self, item_data):
        from items import Item

        _id = item_data[0]
        pet_id = item_data[1]
        mount_id = item_data[2]
        level = item_data[3]
        name = item_data[4]
        quality = item_data[5]
        item_class = item_data[6]
        item_subclass = item_data[7]
        type = item_data[8]
        subtype = item_data[9]
        mean_price = item_data[10]
        sold = item_data[11]
        price = item_data[12]
        if sold is None: sold = 0.0
        if price is None: price = 0.0

        kwargs = {
                    "_id":_id, "pet":{"_id":pet_id}, "mount":{"_id":mount_id}, "level":level,
                    "name":name, "quality":quality, "item_class":item_class,
                    "item_subclass":item_subclass, "type":type, "subtype":subtype,
                    "mean_price":mean_price, "sold":sold, "price":price,
                    "Class": None, "Subclass": None, "Pet": None, "Mount": None
                }

        is_item = pet_id == 0 and mount_id == 0
        is_pet = _id == 82800
        is_mount = pet_id == 0 and not mount_id == 0
        existing_class = item_class in self.live_data["classes"]
        existing_subclass = existing_class and item_subclass in self.live_data["classes"][item_class].subclasses
        existing_pet = is_pet and pet_id in self.live_data["pets"]
        existing_mount = is_mount and mount_id in self.live_data["mounts"]

        if existing_class: kwargs["Class"] = self.live_data["classes"][item_class]

        if existing_subclass: kwargs["Subclass"] = self.live_data["classes"][item_class].subclasses[item_subclass]

        if is_item:
            self.live_data["items"][_id] = Item(**kwargs)

        elif existing_pet:
            kwargs["Pet"] = self.live_data["pets"][pet_id]
            self.live_data["items"][_id][pet_id] = Item(**kwargs)

        elif existing_mount:
            kwargs["Mount"] = self.live_data["mounts"][mount_id]
            self.live_data["items"][_id] = Item(**kwargs)


    def setLiveAuction(self, realm, auction_data):
        from auctions import Auction

        realm_id = auction_data[0]
        _id = auction_data[1]
        item_id = auction_data[2]
        pet_id = auction_data[3]
        quantity = auction_data[4]
        unit_price = auction_data[5]
        time_left = auction_data[6]
        bid = auction_data[7]
        buyout = auction_data[8]
        time_posted = auction_data[9]
        last_updated = auction_data[10]
        kwargs = {
                    "realm_id":realm_id, "_id":_id, "item_id":item_id, "pet_id":pet_id, "quantity":quantity, "unit_price":unit_price,
                    "time_left":time_left, "bid":bid, "buyout":buyout, "time_posted":time_posted, "last_updated":last_updated
                    }
        try: kwargs["Item"] = self.live_data["items"][item_id]
        except: kwargs["Item"] = None

        if item_id == 82800:
            kwargs["Item"] = self.live_data["items"][item_id][pet_id]

        realm.previous_auctions[_id] = Auction(realm, **kwargs)
        return realm.auctions


    def setLiveData(self, request):

        # set mounts
        data = self.database.get("SELECT * from mounts", all=True)
        if len(data) > 0:
            try:
                with concurrent.futures.ThreadPoolExecutor() as exe:
                    [exe.submit(self.setLiveMount, mount) for mount in data]
            except Exception as e: print(e)
        msg = "Done setting live mounts; {} live mounts".format(len(self.live_data["mounts"]))
        self.logger.log(msg=msg)

        # set pets
        data = self.database.get("SELECT * from pets", all=True)
        if len(data) > 0:
            try:
                with concurrent.futures.ThreadPoolExecutor() as exe:
                    [exe.submit(self.setLivePets, pet) for pet in data]
            except Exception as e: print(e)
        msg = "Done setting live pets; {} live pets".format(len(self.live_data["pets"]))
        self.logger.log(msg=msg)

        # set classes
        data = self.database.get("SELECT * from classes", all=True)
        if len(data) > 0:
            try:
                with concurrent.futures.ThreadPoolExecutor() as exe:
                    [exe.submit(self.setLiveClasses, live_class) for live_class in data]
            except Exception as e: print(e)
        msg = "Done setting live classes; {} live classes".format(len(self.live_data["classes"]))
        self.logger.log(msg=msg)

        # set subclasses
        query = "SELECT * from subclasses"
        data = self.database.get(query, all=True)
        if len(data) > 0:
            try:
                with concurrent.futures.ThreadPoolExecutor() as exe:
                    [exe.submit(self.setLiveSubclasses, subclass) for subclass in data]
            except Exception as e: print(e)
        subclasses = [x for x in self.live_data["classes"] for _ in self.live_data["classes"][x].subclasses]
        msg = "Done setting live subclasses; {} live subclasses".format(len(subclasses))
        self.logger.log(msg=msg)

        # set items
        query = """
                    select id, items.pet_id, mount_id, level, name, quality, class_id, subclass_id, type, subtype, mean_price, cast(sum(quantity) as double) as sold, sum(quantity * unit_price) as price
                    from items
                    left join soldauctions on soldauctions.item_id = items.id
    	               and soldauctions.pet_id = items.pet_id
                   group by items.id, items.pet_id
                   order by items.id, items.pet_id
               """
        data = self.database.get(query, True)
        if len(data) > 0:
            try:
                with concurrent.futures.ThreadPoolExecutor() as exe:
                    [exe.submit(self.setLiveItem, item) for item in data]
            except Exception as e: print(e)
        items = len(self.live_data["items"]) - 1
        pets = len(self.live_data["items"][82800])
        total_items = items + pets
        msg = "Done setting live items; {} live items of which {} items and {} pets".format(total_items, items-1, pets)
        self.logger.log(msg=msg)

        # set auctions
        border = datetime.datetime.now() - datetime.timedelta(hours=49)
        for realm in self.realms:
            query = """
                        select * from auctionhouses
                        where realm_id = {}
                            and not auction_id in (
                                select auction_id from soldauctions
                                where realm_id = {}
                                    and partial = 0)
                            and time_posted >= "{}"
                    """.format(realm.id, realm.id, border)
            data = self.database.get(query, all=True)
            if len(data) > 0:
                for auction in data:
                    self.setLiveAuction(realm, auction)
                #try:
                #    with concurrent.futures.ThreadPoolExecutor() as exe:
                #        [exe.submit(setLiveAuction, live_data, auction, logger) for auction in data]
                #except Exception as err: logger.log(msg=err, err=err)
            msg = "Done setting live auctions for realm {}; {} live auctions".format(realm.name, len(realm.previous_auctions.keys()))
            self.logger.log(msg=msg)



    def update(self):
        self.insert_data = {}
        self.update_data = {}



def setTimePosted(posted=None, test=False):
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute_posted = 0
    second_posted = 0
    microsecond_posted = 0
    if test:
        hour = 12
        minute = 30
        second = 30
        micro = 500000
    elif posted:
        time_posted = posted
        minute_posted = time_posted.minute
        second_posted = time_posted.second
        microsecond_posted = time_posted.microsecond
        minute = random.randrange(max(minute_posted, 45), 60)
        second = random.randrange(max(second_posted, 45), 60)
        micro = random.randrange(max(microsecond_posted, 9999999), 1000000)
    else:
        minute = random.randrange(now.minute, 60)
        second = random.randrange(now.second, 60)
        micro = random.randrange(now.microsecond, 1000000)

    time_posted = datetime.datetime(year, month, day, hour, minute, second, micro)
    return time_posted


def setTimeSold(posted=None):
    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    if posted: minute_posted = posted.minute
    else: minute_posted = 0
    minute = random.randrange(max(minute_posted, now.minute+1), 60)
    second = random.randrange(0, now.second + 1)
    micro = random.randrange(0, 1000000)

    time_sold = datetime.datetime(year, month, day, hour, minute, second, micro) - datetime.timedelta(hours=1)

    return time_sold
