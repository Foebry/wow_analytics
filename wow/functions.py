"""extra functions not directly related to any class"""
import datetime
import random
import concurrent.futures



def createAuctionsQuery(insert_data, db, section, realm_id, logger):
    from math import ceil, floor
    begin = section[0]
    end = section[1]
    remaining = end - begin
    auctions = len(insert_data["auctions"][realm_id])

    auctions_query = "INSERT into auctionhouses(realm_id, auction_id, item_id, pet_id, quantity, unit_price, time_left, bid, buyout, time_posted, last_updated) values\n"

    for auction in insert_data["auctions"][realm_id][begin:end]:

        pet_id = 0
        if auction.item_id == 82800: pet_id = auction.pet_id

        auction_values = "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s),\n" %(realm_id, auction.id, auction.item_id, f"{pet_id}", auction.quantity, auction.unit_price, f'"{auction.time_left}"', auction.bid, auction.buyout, f'"{auction.time_posted}"', f'"{auction.last_updated}"')
        auctions_query += auction_values

    auctions_query = auctions_query[:-2] + ";"

    good_section = db.write(auctions_query, logger)
    if not good_section: return createAuctionsQuery(insert_data, db, (begin, floor(remaining/2)), realm_id, logger)

    if end < auctions: return createAuctionsQuery(insert_data, db, (end, auctions), realm_id, logger)

    return logger.log(f"Inserted {auctions} auctions")


def createSoldauctionsQuery(insert_data, db, section, realm_id, logger):
    from math import ceil, floor
    begin = section[0]
    end = section[1]
    remaining = end-begin
    len_sold_auctions = len(insert_data["auctions"][realm_id])


    sold_auctions_query = "INSERT into soldauctions(realm_id, auction_id, item_id, pet_id, quantity, unit_price, time_left, bid, buyout, time_sold, partial) values\n"

    for sold_auction in insert_data["sold_auctions"][realm_id][begin:section]:
        pet_id = 0
        if auction.item_id == 82800: pet_id = auction.pet_id["id"]

        auction_values = "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s),\n" %(realm_id, auction.id, auction.item_id, pet_id, auction.quantity, auction.unit_price, f'"{auction.time_left}"', auction.bid, auction.buyout, f'"{auction.time_sold}"', auction.partial)
        sold_auctions_query += auction_values

    sold_auctions_query = sold_auctions_query[:-2] + ";"

    good_section = db.write(sold_auctions_query, logger)
    if not good_section: return createSoldauctionsQuery(insert_data, db, (begin, floor(remaining/2)), realm_id, logger)

    if end < len_sold_auctions: return createSoldauctionsQuery(insert_data, db, (end, len_sold_auctions), realm_id, logger)

    return logger.log(f"Inserted {sold_auctions} sold auctions")


def createItemsQuery(insert_data, db, section, logger):
    from math import ceil, floor
    times = ceil(len(insert_data))
    insert_items_query = "INSERT INTO items(id, pet_id, mount_id, level, name, quality, class_id, subclass_id, type, subtype, mean_price) VALUES \n  "

    for index in range(len(insert_data["items"])):
        item = insert_data["items"][index]
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
    db.write(insert_items_query, logger)
    items = len(insert_data["items"])
    logger.log(f"Inserted {items} items" )



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
        minute = random.randrange(max(minute_posted, now.minute), 60)
        second = random.randrange(max(second_posted, now.second), 60)
        micro = random.randrange(max(microsecond_posted, now.microsecond), 1000000)
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



def setAuctionData(realm_id, auction_data, live_data, insert_data, update_data, previous_auctions, request, db, logger, test=False):
    """Setting auction data from getAuctionData response. Takes in 4 arguments:
      :arg realm_id: int,
      :arg auction_data: dict,
      :arg live_data: dict,
      :arg previous_auctions: dict"""
    from auctions import Auction

    auctions = []
    for auction in auction_data:
        auction_id = auction["id"]
        item_id = auction["item"]["id"]
        pet = {"_id":0}

        if item_id == 82800:
            pet = {"_id":auction["item"]["pet_species_id"], "quality":auction["item"]["pet_quality_id"], "level":auction["item"]["pet_level"], "breed_id":auction["item"]["pet_breed_id"]}

        quantity = auction["quantity"]
        time_left = auction["time_left"]
        time_posted = setTimePosted()
        last_updated = time_posted

        # all are given
        if "unit_price" in auction and "bid" in auction and "buyout" in auction:
            unit_price = auction["unit_price"] / 10000
            bid = auction["bid"] / 10000
            buyout = auction["buyout"] / 10000

        # bid is missing -> bid = -1
        elif "unit_price" in auction and "buyout" in auction and "bid" not in auctions:
            unit_price = auction["unit_price"] / 10000
            buyout = auction["buyout"] / 10000
            bid = -1

        # unit_price is missing -> unit_price = buyout / quantity
        elif "buyout" in auction and "bid" in auction and "unit_price" not in auction:
            buyout = auction["buyout"] / 10000
            bid = auction["bid"] / 10000
            unit_price = buyout / quantity

        # buyout is missing -> buyout = -1
        elif "unit_price" in auction and "bid" in auction and "buyout" not in auction:
            unit_price = auction["unit_price"] / 10000
            bid = auction["bid"] / 10000
            buyout = -1

        # buyout AND bid are missing -> buyout = unit_price*quantity, bid = -1
        elif "unit_price" in auction and "bid" not in auction and "buyout" not in auction:
            unit_price = auction["unit_price"] / 10000
            bid = -1
            buyout = unit_price * quantity

        # bid and unit_price are missing -> unit_price = buyout / quantity, bid = -1
        elif "buyout" in auction and "unit_price" not in auction and "bid" not in auction:
            buyout = auction["buyout"] / 10000
            unit_price = buyout / quantity
            bid = -1

        # buyout AND unit_price are missing -> buyout = -1, unit_price = bid / quantity
        elif "bid" in auction and "unit_price" not in auction and "buyout" not in auction:
            bid = auction["bid"] / 10000
            unit_price = bid / quantity
            buyout = -1

        args = (realm_id, auction_id, item_id, pet, quantity, unit_price, time_left, bid, buyout, time_posted, last_updated)
        auction = Auction(live_data, logger, previous_auctions, insert_data, update_data, request, db, test, *args)

        print('auctions:', len(insert_data['auctions'][realm_id]), '- items:', len(insert_data['items']), '- classes:', len(insert_data["classes"]), "- pets:", len(insert_data["pets"]), end='\r')
        # for testing purposes
        auctions.append(auction)
    # for testing purposes
    return auctions


def updateData(db, update_data, realm_id, logger):
    """Updates all data to be updated (auctions, items). Takes in 2 arguments:
        :arg database: obj<Database>,
        :arg update_data: dict"""

    update_query = "UPDATE auctionhouses \n"
    update_quantity = "SET\n    quantity = CASE auction_id \n"
    update_time_left = "    time_left = CASE auction_id \n"
    update_bid = "  bid = CASE auction_id \n"
    update_buyout = "   buyout = CASE auction_id \n"
    update_last_updated = " last_updated = CASE auction_id \n"
    where = "WHERE auction_id in ("

    if "auctions" in update_data:
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
            db.execute(update_query)

    # update items
    if "items" in update_data and len(update_data["items"]) > 0:
        update_query = "UPDATE items \n SET mean_price = CASE \n"
        where = "WHERE auction_id in ("
        for item in update_data["items"]:
            update_query += "   when id = %s and pet_id = %s and mount_id = %s and level = %s\n"%(item.id, item.pet_id, item.mount_id, item.level)
            update_query += "   else mean_price"
            where += "%s, "%item.id
        where = where[:-2] + ");"
        update_query += "end\n"
        update_query += where
        db.execute(update_query)



def insertData(db, insert_data, update_data, previous_auctions, realm_id, logger):
    """Writes all sold data, database. Takes in 3 arguments:
        :arg database: obj<Database>,
        :arg insert_data: dict,
        :arg previous_auctions: dict"""

    auctions_to_insert = "auctions" in insert_data and realm_id in insert_data["auctions"] and len(insert_data["auctions"][realm_id]) > 0
    fully_sold_auctions = realm_id in previous_auctions and len(previous_auctions[realm_id]) > 0
    sold_auctions_to_insert = "sold_auctions" in insert_data and len(insert_data["sold_auctions"][realm_id]) > 0
    items_to_insert = "items" in insert_data and len(insert_data["items"]) > 0

    if auctions_to_insert:
        auctions = len(insert_data["auctions"][realm_id])
        section = (0, auctions)
        createAuctionsQuery(insert_data, db, section, realm_id, logger)

    # adding fully sold auctions to insert_data
    if fully_sold_auctions:
        from auctions import SoldAuction
        for auction_id in previous_auctions[realm_id]:
            auction = previous_auctions[realm_id][auction_id]
            args = (auction, realm_id, auction.id, auction.item_id, auction.pet_id, auction.quantity, auction.unit_price, auction.time_left, auction.bid, auction.buyout, auction.time_posted, False)
            sold_auction = SoldAuction(insert_data, update_data, *args)

    if sold_auctions_to_insert:
        soldauctions = len(insert_data["sold_auctions"][realm_id])
        section = (0, soldauctions)
        createSoldauctionsQuery(insert_data, db, section, realm_id, logger)

    if items_to_insert:
        items = len(insert_data["items"])
        sections = (0, items)
        createItemsQuery(insert_data, db, section, logger)

    # inserting classes
    if "classes" in insert_data and len(insert_data["classes"]) > 0:
        insert_classes_query = "INSERT INTO classes(id, name) VALUES \n "

        for insert_class in insert_data["classes"]:
            class_values = "(%s, %s),\n "%(insert_class.id, f'"{insert_class.name}"')
            insert_classes_query += class_values

        insert_classes_query = insert_classes_query[:-3] + ";"
        db.write(insert_classes_query, logger)
        classes = len(insert_data["classes"])
        logger.log(f"Inserted {classes} classes")

    # insert subclasses
    if "subclasses" in insert_data and len(insert_data["subclasses"]) > 0:
        insert_subclass_query = "INSERT INTO subclasses(Class_id, id, name) VALUES\n    "

        for subclass in insert_data["subclasses"]:
            subclass_values = "(%s, %s, %s),\n  "%(subclass.class_id, subclass.subclass_id, f'"{subclass.name}"')
            insert_subclass_query += subclass_values
        insert_subclass_query = insert_subclass_query[:-4] + ";"

        db.write(insert_subclass_query, logger)
        subclasses = len(insert_data["subclasses"])
        logger.log(f"Inserted {subclasses} subclasses")

    # insert pets
    if "pets" in insert_data and len(insert_data["pets"]) > 0:
        insert_pets_query = "INSERT INTO pets(ID, name, type, source) VALUES \n "

        for pet in insert_data["pets"]:
            pet_values = "(%s, %s, %s, %s), \n  "%(pet.id, f'"{pet.name}"', f'"{pet.type}"', f'"{pet.source}"')
            insert_pets_query += pet_values

        insert_pets_query = insert_pets_query[:-5] + ";"
        db.write(insert_pets_query, logger)
        pets = len(insert_data["pets"])
        logger.log(f"Inserted {pets} pets")

    # insert mounts
    if "mounts" in insert_data and len(insert_data["mounts"]) > 0:
        insert_mounts_query = "INSERT INTO mounts(id, name, source, faction) VALUES \n  "

        for mount in insert_data["mounts"]:
            mount_values = "(%s, %s, %s, %s), \n    " %(mount.id, f'"{mount.name}"', f'"{mount.source}"', f'"{mount.faction}"')
            insert_mounts_query += mount_values

        insert_mounts_query = insert_mounts_query[:-7] + ";"
        db.write(insert_mounts_query, logger)
        mounts = len(insert_data["mounts"])
        logger.log(f"Inserted {mounts} mounts")

    # insert prices
    if "prices" in insert_data and len(insert_data["prices"]) > 0:
        print("insertData section prices")
        for price_update in insert_data["prices"]: db.write(price_update, logger)


def setLiveMounts(live_data, mount_data, logger):
    from mounts import Mount

    kwargs = {"_id":mount_data[0], "name":mount_data[1], "source":mount_data[2], "faction":mount_data[3]}
    if "mounts" in live_data: live_data["mounts"][mount_data[0]] = Mount(logger, **kwargs)
    else: live_data["mounts"] = {mount_data[0]:Mount(logger, **kwargs)}

    return live_data["mounts"]


def setLivePets(live_data, pet_data, logger):
    from pets import Pet

    kwargs = {"_id":pet_data[0], "name": pet_data[1], "type":pet_data[2], "source":pet_data[3], "faction":"Factionless"}
    live_data["pets"][pet_data[0]] = Pet(logger, **kwargs)

    return live_data["pets"]


def setLiveClasses(live_data, class_data, logger):
    from classes import Class

    kwargs = {"_id":class_data[0], "name": class_data[1], "subclasses":{}}
    if "classes" in live_data: live_data["classes"][class_data[0]] = Class(logger, **kwargs)
    else: live_data["classes"] = {class_data[0]: Class(logger, **kwargs)}

    return live_data["classes"]


def setLiveSubclasses(live_data, subclass_data, logger):
    from classes import Subclass

    kwargs = {"class_id":subclass_data[0], "subclass_id":subclass_data[1], "name": subclass_data[2]}
    live_data["classes"][subclass_data[0]].subclasses[subclass_data[1]] = Subclass(logger, **kwargs)

    return live_data["classes"]


def setLiveItems(db, live_data, item_data, logger):
    from items import Item

    data = db.get("SELECT sum(quantity)as quantity, sum(quantity * unit_price) as price from soldauctions where item_id = %s"%(item_data[0]), logger)
    sold = data[0]
    price = data[1]
    if sold is None: sold = 0.0
    if price is None: price = 0.0
    kwargs = {"_id":item_data[0], "pet":{"_id":item_data[1]}, "mount":{"_id":item_data[2]}, "level": item_data[3], "name":item_data[4], "quality":item_data[5], "item_class":item_data[6], "item_subclass":item_data[7], "type":item_data[8], "subtype":item_data[9], "mean_price":item_data[10], "sold":sold, "price":price}

    is_item = kwargs["pet"]["_id"] == 0 and kwargs["mount"]["_id"] == 0
    is_pet = kwargs["_id"] == 82800
    is_mount = kwargs["pet"]["_id"] == 0 and not kwargs["mount"]["_id"] == 0
    existing_class = kwargs["item_class"] in live_data["classes"]
    existing_subclass = kwargs["item_class"] in live_data["classes"] and kwargs["item_subclass"] in live_data["classes"][kwargs["item_class"]].subclasses
    existing_pet = is_pet and kwargs["pet"]["_id"] in live_data["pets"]
    existing_mount = is_mount and kwargs["mount"]["_id"] in live_data["mounts"]


    if existing_class: kwargs["Class"] = live_data["classes"][kwargs["item_class"]]

    if existing_subclass: kwargs["Subclass"] = live_data["classes"][kwargs["item_class"]].subclasses[kwargs["item_subclass"]]

    if is_item:
        kwargs["Pet"] = None
        kwargs["Mount"] = None
        live_data["items"][item_data[0]] = Item(logger, **kwargs)

    elif existing_pet:
        kwargs["Pet"] = live_data["pets"][kwargs["pet"]["_id"]]
        kwargs["Mount"] = None
        live_data["items"][item_data[0]] = {}
        live_data["items"][item_data[0]][kwargs["pet"]["_id"]] = Item(logger, **kwargs)

    elif existing_mount:
        kwargs["Pet"] = None
        kwargs["Mount"] = live_data["mounts"][kwargs["mount"]["_id"]]
        live_data["items"][item_data[0]] = Item(logger, **kwargs)


    return live_data["items"]


def setLiveAuctions(live_data, auction_data, logger, request):
    from auctions import Auction

    kwargs = {"realm_id":auction_data[0], "_id":auction_data[1], "item_id":auction_data[2], "pet_id":auction_data[3], "quantity":auction_data[4], "unit_price":auction_data[5], "time_left":auction_data[6], "bid":auction_data[7], "buyout":auction_data[8], "time_posted":auction_data[9], "last_updated":auction_data[10]}
    realm_id = auction_data[0]
    auction_id = auction_data[1]
    if "auctions" in live_data:
        if realm_id in live_data["auctions"]:
            live_data["auctions"][realm_id][auction_id] = Auction(live_data, logger, request=request, **kwargs)
        else:
            live_data["auctions"][realm_id] = {}
            live_data["auctions"][realm_id][auction_id] = Auction(live_data, logger, request=request, **kwargs)
    else:
        live_data["auctions"] = {}
        live_data["auctions"][realm_id] = {}
        live_data["auctions"][realm_id][auction_id] = Auction(live_data, logger, request=request, **kwargs)

    return live_data["auctions"]


def setLiveData(realm_id, db, logger, request):
    live_data = {"auctions":{realm_id:{}}, "items":{}, "classes":{}, "pets":{}, "mounts":{}}

    # set mounts
    data = db.get("SELECT * from mounts", logger, True)
    if len(data) > 0:
        #for mount in data: setLiveMounts(live_data, mount)
        with concurrent.futures.ThreadPoolExecutor() as exe:
            [exe.submit(setLiveMounts, live_data, mount, logger) for mount in data]
    else: live_data["mounts"] = {}

    # set pets
    data = db.get("SELECT * from pets", logger, True)
    if len(data) > 0:
        #for pet in data: setLivePets(live_data, pet, logger)
        with concurrent.futures.ThreadPoolExecutor() as exe:
            [exe.submit(setLivePets, live_data, pet, logger) for pet in data]
    else: live_data["pets"] = {}

    # set classes
    data = db.get("SELECT * from classes", logger, True)
    if len(data) > 0:
        with concurrent.futures.ThreadPoolExecutor() as exe:
            [exe.submit(setLiveClasses, live_data, live_class, logger) for live_class in data]
    else: live_data["classes"] = {}

    # set subclasses
    data = db.get("SELECT * from subclasses", logger, True)
    if len(data) > 0:
        with concurrent.futures.ThreadPoolExecutor() as exe:
            [exe.submit(setLiveSubclasses, live_data, subclass, logger) for subclass in data]

    # set items
    data = db.get("SELECT * from items", logger, True)
    if len(data) > 0:
        with concurrent.futures.ThreadPoolExecutor() as exe:
            [exe.submit(setLiveItems, db, live_data, item, logger) for item in data]
    else: live_data["items"] = {}

    # set auctions
    border = datetime.datetime.now() - datetime.timedelta(hours=24)
    query = "SELECT * from auctionhouses where last_updated > %s" %f'"{border}"'
    data = db.get(query, logger, True)
    if len(data) > 0:
        try:
            with concurrent.futures.ThreadPoolExecutor() as exe:
                [exe.submit(setLiveAuctions, live_data, auction, logger, request) for auction in data]
        except Exception as err: logger.log(err, type(err))

    return live_data