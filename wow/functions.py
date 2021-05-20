"""extra functions not directly related to any class"""
import datetime
import random
import concurrent.futures



def isValidSoldAuction(live_data, sold_auction, auctions_to_check, logger):
    item = sold_auction.auction.Item
    try: not_overpriced = item.mean_price == 0 or sold_auction.unit_price < 5*item.mean_price and sold_auction.unit_price < 9999999.9999
    except Exception as e:
        logger.log(True, msg="item = {}".format(sold_auction.auction.Item))
        return
    valid = sold_auction.time_left != "SHORT" and not_overpriced

    for soldauction in auctions_to_check:
        cheaper = sold_auction.unit_price < soldauction.unit_price
        got_undercut = sold_auction.unit_price == soldauction.unit_price and sold_auction.auction.time_posted < soldauction.auction.time_posted

        if not cheaper or got_undercut: return False

    if valid:
        del live_data["auctions"][sold_auction.realm_id][sold_auction.auction.id]
        return True

    return False



def createInsertAuctionsQuery(insert_data, db, section, realm_id, logger):
    from math import floor

    print(" "*100, end="\r")
    print("inserting auctions {} - {}".format(section[0], section[1]), end="\r")

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
    if not good_section: return createInsertAuctionsQuery(insert_data, db, (begin, floor(begin+remaining/2)), realm_id, logger)

    if end < auctions: return createInsertAuctionsQuery(insert_data, db, (end, auctions), realm_id, logger)

    return logger.log(msg=f"Inserted {auctions} auctions")


def createUpdateAuctionsQuery(update_data, db, section, realm_id, logger):
    from math import floor
    print(" "*100, end="\r")
    print("updating auctions {} - {}".format(section[0], section[1]), end="\r")

    begin = section[0]
    end = section[1]
    remaining = end - begin
    auctions = len(update_data["auctions"][realm_id])

    update_query = "UPDATE auctionhouses \n"
    update_quantity = "SET\n    quantity = CASE auction_id \n"
    update_time_left = "    time_left = CASE auction_id \n"
    update_bid = "  bid = CASE auction_id \n"
    update_buyout = "   buyout = CASE auction_id \n"
    update_last_updated = " last_updated = CASE auction_id \n"
    where = "WHERE auction_id in ("

    for auction in update_data["auctions"][realm_id][begin:end]:
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
    where += ");"

    update_query = update_query + update_quantity + update_time_left + update_bid + update_buyout + update_last_updated + where

    good_section = db.update(update_query, logger)
    if not good_section: return  createUpdateAuctionsQuery(update_data, db, (begin, floor(begin+remaining/2)), realm_id, logger)

    if end < auctions: return createUpdateAuctionsQuery(update_data, db, (end, auctions), realm_id, logger)

    return logger.log(msg=f"Updated {auctions} auctions")



def createSoldauctionsQuery(insert_data, db, section, realm_id, logger):
    from math import floor

    print(" "*100, end="\r")
    print("inserting soldauctions {} - {}".format(section[0], section[1]), end="\r")

    begin = section[0]
    end = section[1]
    remaining = end - begin
    len_sold_auctions = len(insert_data["sold_auctions"][realm_id])


    sold_auctions_query = "INSERT into soldauctions(realm_id, auction_id, item_id, pet_id, quantity, unit_price, time_left, bid, buyout, time_sold, partial) values\n"

    for sold_auction in insert_data["sold_auctions"][realm_id][begin:end]:
        pet_id = 0
        if sold_auction.item_id == 82800: pet_id = sold_auction.pet_id

        auction_values = "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s),\n" %(realm_id, sold_auction.id, sold_auction.item_id, pet_id, sold_auction.quantity, sold_auction.unit_price, f'"{sold_auction.time_left}"', sold_auction.bid, sold_auction.buyout, f'"{sold_auction.time_sold}"', sold_auction.partial)
        sold_auctions_query += auction_values

    sold_auctions_query = sold_auctions_query[:-2] + ";"

    good_section = db.write(sold_auctions_query, logger)
    if not good_section: return createSoldauctionsQuery(insert_data, db, (begin, floor(begin+remaining/2)), realm_id, logger)

    if end < len_sold_auctions: return createSoldauctionsQuery(insert_data, db, (end, len_sold_auctions), realm_id, logger)

    return logger.log(msg=f"Inserted {len_sold_auctions} sold auctions")


def createInsertItemsQuery(insert_data, db, section, logger):
    from math import floor

    print(" "*100, end="\r")
    print("inserting items {} - {}".format(section[0], section[1]), end="\r")

    begin = section[0]
    end = section[1]
    remaining = end - begin
    items = len(insert_data["items"])

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

    good_section = db.write(insert_items_query, logger)
    if not good_section: return createInsertItemsQuery(insert_data, db, (start, floor(begin+remaining/2)), logger)

    if end > items: return createInsertItemsQuery(insert_data, db, (end, items), logger)

    return logger.log(msg=f"Inserted {items} items" )


def createUpdateItemsQuery(update_data, db, section, logger):
    from math import floor
    # from ErrorHandler import RaiseError

    print(" "*100, end="\r")
    print("updateing items {} - {}".format(section[0], section[1]), end="\r")

    begin = section[0]
    end = section[1]

    # if begin > end: RaiseError.ValueError("section[0] is greater then section[1] for createUpdateItemsQuery functions.py")

    remaining = end - begin
    items = len(update_data["items"])

    update_query = "UPDATE items \n SET mean_price = CASE \n"
    where = "where id in ("

    for item in update_data["items"][begin:end]:
        update_query += "   when id = {} and pet_id = {} and mount_id = {} and level = {} then {}\n".format(item.id, item.pet_id, item.mount_id, item.level, item.mean_price)
        where += "{}, ".format(item.id)

    where = where[:-2] + ");"
    update_query += "   else mean_price \n end\n"
    update_query += where

    good_section = db.update(update_query, logger)
    if not good_section: return createUpdateItemsQuery(update_data, db, (begin, floor(begin+remaining/2)), logger)

    if end < items: return createUpdateItemsQuery(update_data, db, (end, items), logger)

    return logger.log(msg=f"Updated {items} items")


def createInsertMountsQuery(insert_data, db, section, logger):
    from math import floor

    print(" "*100, end="\r")
    print("inserting mounts {} - {}".format(section[0], section[1]), end="\r")

    begin = section[0]
    end = section[1]

    remaining = end - begin
    mounts = len(insert_data["mounts"])

    insert_mounts_query = "INSERT INTO mounts(id, name, source, faction) VALUES \n  "

    for mount in insert_data["mounts"]:
        mount_values = "(%s, %s, %s, %s), \n    " %(mount.id, f'"{mount.name}"', f'"{mount.source}"', f'"{mount.faction}"')
        insert_mounts_query += mount_values

    insert_mounts_query = insert_mounts_query[:-7] + ";"

    good_section = db.write(insert_mounts_query, logger)
    if not good_section: return createInsertMountsQuery(insert_data, db, (begin, floor(begin+remaining/2)), logger)

    if end < mounts: return createInsertMountsQuery(insert_data, db, (end, mounts), logger)

    return logger.log(msg=f"Inserted {mounts} mounts")


def createInsertPetsQuery(insert_data, db, section, logger):
    from math import floor

    print(" "*100, end="\r")
    print("inserting pets {} - {}".format(section[0], section[1]), end="\r")

    begin = section[0]
    end = section[1]

    remaining = end - begin
    pets = len(insert_data["pets"])

    insert_pets_query = "INSERT INTO pets(ID, name, type, source) VALUES \n "

    for pet in insert_data["pets"]:
        pet_values = "(%s, %s, %s, %s), \n  "%(pet.id, f'"{pet.name}"', f'"{pet.type}"', f'"{pet.source}"')
        insert_pets_query += pet_values

    insert_pets_query = insert_pets_query[:-5] + ";"

    good_section = db.write(insert_pets_query, logger)
    if not good_section: return createInsertPetsQuery(insert_data, db, (begin, floor(begin+remaining/2)), logger)

    if end < pets: return createInsertPetsQuery(insert_data, db, (end, pets), logger)

    return logger.log(msg=f"Inserted {pets} pets")


def createInsertClassesQuery(insert_data, db, section, logger):
    from math import floor

    print(" "*100, end="\r")
    print("inserting classes {} - {}".format(section[0], section[1]), end="\r")

    begin = section[0]
    end = section[1]

    remaining = end - begin
    classes = len(insert_data["classes"])

    insert_classes_query = "INSERT INTO classes(id, name) VALUES \n "

    for insert_class in insert_data["classes"]:
        class_values = "(%s, %s),\n "%(insert_class.id, f'"{insert_class.name}"')
        insert_classes_query += class_values

    insert_classes_query = insert_classes_query[:-3] + ";"

    good_section = db.write(insert_classes_query, logger)
    if not good_section: return creatInsertClassesQuery(insert_data, db, section, logger)

    if end < classes: return createInsertClassesQuery(insert_data, db, section, logger)

    return logger.log(msg=f"Inserted {classes} classes")



def createInsertSubclassesQuery(insert_data, db, section, logger):
    from math import floor

    print(" "*100, end="\r")
    print("insertsubclasses {} - {}".format(section[0], section[1]), end="\r")

    begin = section[0]
    end = section[1]

    remaining = end - begin
    subclasses = len(insert_data["subclasses"])


    insert_subclass_query = "INSERT INTO subclasses(Class_id, id, name) VALUES\n    "

    for subclass in insert_data["subclasses"]:
        subclass_values = "(%s, %s, %s),\n  "%(subclass.class_id, subclass.subclass_id, f'"{subclass.name}"')
        insert_subclass_query += subclass_values

    insert_subclass_query = insert_subclass_query[:-4] + ";"

    good_section = db.write(insert_subclass_query, logger)
    if not good_section: return createInsertSubclassesQuery(insert_data, db, section, logger)

    if end < subclasses: return createInsertSubclassesQuery(insert_data, db, section, logger)

    return logger.log(msg=f"Inserted {subclasses} subclasses")



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

        print("{}/{} auctions handled".format(len(auctions), len(auction_data)), end='\r')
        # for testing purposes
        auctions.append(auction)
    # for testing purposes
    return auctions


def updateData(db, update_data, realm_id, logger):
    """Updates all data to be updated (auctions, items). Takes in 2 arguments:
        :arg database: obj<Database>,
        :arg update_data: dict"""

    auctions_to_update = "auctions" in update_data and realm_id in update_data["auctions"] and len(update_data["auctions"][realm_id]) > 0
    items_to_update = "items" in update_data and len(update_data["items"]) > 0
    realms_to_update = "realms" in update_data and len(update_data["realms"]) > 0

    if auctions_to_update:
        end = len(update_data["auctions"][realm_id])
        createUpdateAuctionsQuery(update_data, db, (0, end), realm_id, logger)

    if items_to_update:
        end = len(update_data["items"])
        createUpdateItemsQuery(update_data, db, (0, end), logger)

    if realms_to_update:
        for realm in update_data["realms"]: realm.update(db, logger)



def insertData(db, live_data, insert_data, update_data, previous_auctions, realm_id, logger):
    """
        Function responsible to write all data into the database.
    """

    auctions_to_insert = "auctions" in insert_data and realm_id in insert_data["auctions"] and len(insert_data["auctions"][realm_id]) > 0
    fully_sold_auctions = realm_id in previous_auctions and len(previous_auctions[realm_id]) > 0
    items_to_insert = "items" in insert_data and len(insert_data["items"]) > 0
    item_prices_to_insert = "items" in update_data and len(update_data["items"]) > 0
    mounts_to_insert = "mounts" in insert_data and len(insert_data["mounts"]) > 0
    pets_to_insert = "pets" in insert_data and len(insert_data["pets"]) > 0
    classes_to_insert = "classes" in insert_data and len(insert_data["classes"]) > 0
    subclasses_to_insert = "subclasses" in insert_data and len(insert_data["subclasses"]) > 0

    if mounts_to_insert:
        mounts = len(insert_data["mounts"])
        section = (0, mounts)
        createInsertMountsQuery(insert_data, db, section, logger)

    if pets_to_insert:
        pets = len(insert_data["pets"])
        section = (0, pets)
        createInsertPetsQuery(insert_data, db, section, logger)

    if classes_to_insert:
        classes = len(insert_data["classes"])
        section = (0, classes)
        createInsertClassesQuery(insert_data, db, section, logger)

    if subclasses_to_insert:
        subclasses = len(insert_data["subclasses"])
        section = (0, subclasses)
        createInsertSubclassesQuery(insert_data, db, section, logger)

    if items_to_insert:
        items = len(insert_data["items"])
        section = (0, items)
        createInsertItemsQuery(insert_data, db, section, logger)

    if auctions_to_insert:
        auctions = len(insert_data["auctions"][realm_id])
        section = (0, auctions)
        createInsertAuctionsQuery(insert_data, db, section, realm_id, logger)

    # adding fully sold auctions to insert_data
    if fully_sold_auctions:
        from auctions import SoldAuction
        for auction_id in previous_auctions[realm_id]:
            auction = previous_auctions[realm_id][auction_id]
            args = (auction, realm_id, auction.id, auction.item_id, auction.pet_id, auction.quantity, auction.unit_price, auction.time_left, auction.bid, auction.buyout, auction.time_posted, False)
            sold_auction = SoldAuction(live_data, insert_data, update_data, logger, *args)

    sold_auctions_to_insert = "sold_auctions" in insert_data and len(insert_data["sold_auctions"][realm_id]) > 0

    if sold_auctions_to_insert:
        soldauctions = len(insert_data["sold_auctions"][realm_id])
        section = (0, soldauctions)
        createSoldauctionsQuery(insert_data, db, section, realm_id, logger)

    # insert prices
    if item_prices_to_insert:
        insert_string = "INSERT INTO item_prices (item_id, pet_id, time, value) VALUES \n "

        for index in range(len(update_data["items"])):
            item = update_data["items"][index]
            price_values = "(%s, %s, %s, %s), \n" %(item.id, item.pet_id, f'"{datetime.datetime.now() - datetime.timedelta(hours=1)}"', item.mean_price)
            insert_string += price_values

        insert_string = insert_string[:-3] + ";"
        db.write(insert_string, logger)
        insert_strings = len(update_data["items"])
        logger.log(msg="Inserted %s item_price changes" %insert_strings)


def setLiveMount(live_data, mount_data, logger):
    from mounts import Mount

    _id = mount_data[0]
    name = mount_data[1]
    source = mount_data[2]
    faction = mount_data[3]

    kwargs = {"_id":_id, "name":name, "source":source, "faction":faction}

    live_data["mounts"][_id] = Mount(logger, **kwargs)


def setLivePets(live_data, pet_data, logger):
    from pets import Pet

    _id = pet_data[0]
    name = pet_data [1]
    type = pet_data[2]
    source = pet_data[3]
    faction = pet_data[4]

    kwargs = {"_id":_id, "name": name, "type":type, "source":source, "faction":faction}

    live_data["pets"][_id] = Pet(logger, **kwargs)


def setLiveClasses(live_data, class_data, logger):
    from classes import Class

    _id = class_data[0]
    name = class_data[1]

    kwargs = {"_id":_id, "name": name, "subclasses":{}}

    live_data["classes"][_id] = Class(logger, **kwargs)


def setLiveSubclasses(live_data, subclass_data, logger):
    from classes import Subclass

    class_id = subclass_data[0]
    _id = subclass_data[1]
    name = subclass_data[2]

    kwargs = {"class_id":class_id, "subclass_id":_id, "name": name}

    live_data["classes"][class_id].subclasses[_id] = Subclass(logger, **kwargs)


def setLiveItem(db, live_data, item_data, logger):
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
                "mean_price":mean_price, "sold":sold, "price":price
            }

    is_item = pet_id == 0 and mount_id == 0
    is_pet = _id == 82800
    is_mount = pet_id == 0 and not mount_id == 0
    existing_class = item_class in live_data["classes"]
    existing_subclass = existing_class and item_subclass in live_data["classes"][item_class].subclasses
    existing_pet = is_pet and pet_id in live_data["pets"]
    existing_mount = is_mount and mount_id in live_data["mounts"]

    if existing_class: kwargs["Class"] = live_data["classes"][item_class]

    if existing_subclass: kwargs["Subclass"] = live_data["classes"][item_class].subclasses[item_subclass]

    if is_item:
        kwargs["Pet"] = None
        kwargs["Mount"] = None
        live_data["items"][_id] = Item(logger, **kwargs)

    elif existing_pet:
        kwargs["Pet"] = live_data["pets"][pet_id]
        kwargs["Mount"] = None
        live_data["items"][_id][pet_id] = Item(logger, **kwargs)

    elif existing_mount:
        kwargs["Pet"] = None
        kwargs["Mount"] = live_data["mounts"][mount_id]
        live_data["items"][_id] = Item(logger, **kwargs)


def setLiveAuction(live_data, auction_data, logger):
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
    try: kwargs["Item"] = live_data["items"][item_id]
    except: kwargs["Item"] = None

    if item_id == 82800:
        kwargs["Item"] = live_data["items"][item_id][pet_id]

    live_data["auctions"][realm_id][_id] = Auction(live_data, logger, **kwargs)
    return live_data["auctions"]


def setLiveData(realm_id, db, logger, request):
    live_data = {"auctions":{realm_id:{}}, "items":{82800:{}}, "classes":{}, "pets":{}, "mounts":{}}

    # set mounts
    data = db.get("SELECT * from mounts", logger, True)
    if len(data) > 0:
        #for mount in data: setLiveMounts(live_data, mount)
        try:
            with concurrent.futures.ThreadPoolExecutor() as exe:
                [exe.submit(setLiveMount, live_data, mount, logger) for mount in data]
        except Exception as e: print(e)
    msg = "Done setting live mounts; {} live mounts".format(len(live_data["mounts"]))
    logger.log(msg=msg)

    # set pets
    data = db.get("SELECT * from pets", logger, True)
    if len(data) > 0:
        #for pet in data: setLivePets(live_data, pet, logger)
        try:
            with concurrent.futures.ThreadPoolExecutor() as exe:
                [exe.submit(setLivePets, live_data, pet, logger) for pet in data]
        except Exception as e: print(e)
    msg = "Done setting live pets; {} live pets".format(len(live_data["pets"]))
    logger.log(msg=msg)

    # set classes
    data = db.get("SELECT * from classes", logger, True)
    if len(data) > 0:
        try:
            with concurrent.futures.ThreadPoolExecutor() as exe:
                [exe.submit(setLiveClasses, live_data, live_class, logger) for live_class in data]
        except Exception as e: print(e)
    msg = "Done setting live classes; {} live classes".format(len(live_data["classes"]))
    logger.log(msg=msg)

    # set subclasses
    query = "SELECT * from subclasses"
    data = db.get(query, logger, True)
    if len(data) > 0:
        try:
            with concurrent.futures.ThreadPoolExecutor() as exe:
                [exe.submit(setLiveSubclasses, live_data, subclass, logger) for subclass in data]
        except Exception as e: print(e)
    subclasses = [x for x in live_data["classes"] for _ in live_data["classes"][x].subclasses]
    msg = "Done setting live subclasses; {} live subclasses".format(len(subclasses))
    logger.log(msg=msg)

    # set items
    query = """
                select id, items.pet_id, mount_id, level, name, quality, class_id, subclass_id, type, subtype, mean_price, cast(sum(quantity) as double) as sold, sum(quantity * unit_price) as price
                from items
                left join soldauctions on soldauctions.item_id = items.id
	               and soldauctions.pet_id = items.pet_id
               group by items.id, items.pet_id
               order by items.id, items.pet_id
           """
    data = db.get(query, logger, True)
    if len(data) > 0:
        try:
            with concurrent.futures.ThreadPoolExecutor() as exe:
                [exe.submit(setLiveItem, db, live_data, item, logger) for item in data]
        except Exception as e: print(e)
    items = len(live_data["items"]) - 1
    pets = len(live_data["items"][82800])
    total_items = items + pets
    msg = "Done setting live items; {} live items of which {} items and {} pets".format(total_items, items-1, pets)
    logger.log(msg=msg)

    # set auctions
    border = datetime.datetime.now() - datetime.timedelta(hours=24)
    query = """
                select * from auctionhouses
                   where not auction_id in (
	                 select auction_id from soldauctions
                     where partial = 0)
            """.format(border)
    data = db.get(query, logger, True)
    if len(data) > 0:
        for auction in data:
            setLiveAuction(live_data, auction, logger)
        #try:
        #    with concurrent.futures.ThreadPoolExecutor() as exe:
        #        [exe.submit(setLiveAuction, live_data, auction, logger) for auction in data]
        #except Exception as err: logger.log(msg=err, err=err)
    msg = "Done setting live auctions; {} live auctions".format(len(live_data["auctions"][realm_id]))
    logger.log(msg=msg)

    return live_data
