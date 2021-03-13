"""tests for functions not directly related to any objects"""
from Wow_Analytics.scripts.functions import setTimePosted
from Wow_Analytics.scripts.functions import setAuctionData
from Wow_Analytics.scripts.auctions import Auction, SoldAuction
from Wow_Analytics.scripts.functions import insertAuctions
from Databases.scripts.SQL import SQL
import unittest
import datetime



class FunctionTest(unittest.TestCase):
    def test_setTimePosted(self):
        time_posted = setTimePosted(True)
        self.assertEqual(f"{datetime.datetime.now().date()} 12:30:30.500", time_posted)


    @staticmethod
    def init():
        database.execute("DELETE FROM auctionhouses;")
        database.execute(" DELETE FROM soldauctions;")
        update_data = {}
        previous_auctions = {1096:{}}
        sold_data = {}
        live_data = {"auctions":{1096:{}},
                     "items": {},
                     "classes": {},
                     "pets": {},
                     "mounts": {}}
        # creating auction data
        auction_data_1 = [{"id":1, "item":{"id":35}, "quantity":5, "time_left":"LONG", "unit_price":50, "bid":25, "buyout":250}, # complete
                          {"id":2, "item":{"id":35}, "quantity":5, "time_left":"LONG", "unit_price":50, "buyout":250},             # missing bid
                          {"id":3, "item":{"id":35}, "quantity":5, "time_left":"LONG", "unit_price":50, "bid":25},                 # missing buyout
                          {"id":4, "item":{"id":35}, "quantity":1, "time_left":"LONG", "bid":25, "buyout":50},                     # missing unit_price with quantity = 1
                          {"id":5, "item":{"id":35}, "quantity":5, "time_left":"LONG", "bid":25, "buyout":250},                    # missing unit_price with quantity > 1
                          {"id":6, "item":{"id":35}, "quantity":1, "time_left":"LONG", "unit_price":50},                           # missing bid and buyout with quantity = 1
                          {"id":7, "item":{"id":35}, "quantity":5, "time_left":"LONG", "unit_price":50},                           # missing bid and buyout with quantity > 1
                          {"id":8, "item":{"id":35}, "quantity":1, "time_left":"LONG", "buyout":50},                               # missing bid and unit_price with quantity = 1
                          {"id":9, "item":{"id":35}, "quantity":5, "time_left":"LONG", "buyout":250},                              # missing bid and unit_price with quantity > 1
                          {"id":10, "item":{"id":35}, "quantity":1, "time_left":"LONG", "bid":25},                                 # missing unit_price and buyout with quantity = 1
                          {"id":11, "item":{"id":35}, "quantity":5, "time_left":"LONG", "bid":25},                                 # missing unit_price and buyout with quantity > 1
                          {"id":12, "item":{"id":82800}, "quantity":1, "time_left":"LONG", "unit_price":100, "bid":50, "buyout":100, "pet_species_id":17, "pet_quality_id":2, "pet_level":25, "pet_breed_id":2},  # pet
                          {"id":13, "item":{"id":35}, "quantity":10, "time_left":"MEDIUM", "unit_price":50, "bid":0, "buyout":500},   # to be sold partially
                          {"id":14, "item":{"id":35}, "quantity":2, "time_left":"LONG", "unit_price":50, "bid":0, "buyout":100},      # to be sold completely
                          {"id":15, "item":{"id":35}, "quantity":2, "time_left":"MEDIUM", "unit_price":9999999.9999, "bid":0, "buyout":19999999.9998}, # too expensive to sell
                          {"id":16, "item":{"id":35}, "quantity":2, "time_left":"SHORT", "unit_price":50, "bid":0, "buyout":100}] # to be fully sold but duration_left = "SHORT"

        values_1 = [
                    [1096, 1, 35, None, 5, 50, "LONG", 25, 250],
                    [1096, 2, 35, None, 5, 50, "LONG", -1, 250],
                    [1096, 3, 35, None, 5, 50, "LONG", 25, -1],
                    [1096, 4, 35, None, 1, 50, "LONG", 25, 50],
                    [1096, 5, 35, None, 5, 50, "LONG", 25, 250],
                    [1096, 6, 35, None, 1, 50, "LONG", -1, 50],
                    [1096, 7, 35, None, 5, 50, "LONG", -1, 250],
                    [1096, 8, 35, None, 1, 50, "LONG", -1, 50],
                    [1096, 9, 35, None, 5, 50, "LONG", -1, 250],
                    [1096, 10, 35, None, 1, 25, "LONG", 25, -1],
                    [1096, 11, 35, None, 5, 5, "LONG", 25, -1],
                    [1096, 12, 82800, {"id":17, "quality_id":2, "level":25, "breed_id":2}, 1, 100, "LONG", 50, 100],
                    [1096, 13, 35, None, 10, 50, "MEDIUM", 0, 500],
                    [1096, 14, 35, None, 2, 50, "LONG", 0, 100],
                    [1096, 15, 35, None, 2, 9999999.9999, "MEDIUM", 0, 19999999.9998],
                    [1096, 16, 35, None, 2, 50, "SHORT", 0, 100]
                   ]

        auction_data_2 = [
                          {"id":1, "item":{"id":35}, "quantity":5, "time_left":"LONG", "unit_price":50, "bid":25, "buyout":250}, # complete
                          {"id":2, "item":{"id":35}, "quantity":5, "time_left":"LONG", "unit_price":50, "buyout":250},             # missing bid
                          {"id":3, "item":{"id":35}, "quantity":5, "time_left":"LONG", "unit_price":50, "bid":25},                 # missing buyout
                          {"id":4, "item":{"id":35}, "quantity":1, "time_left":"LONG", "bid":25, "buyout":50},                     # missing unit_price with quantity = 1
                          {"id":5, "item":{"id":35}, "quantity":5, "time_left":"LONG", "bid":25, "buyout":250},                    # missing unit_price with quantity > 1
                          {"id":6, "item":{"id":35}, "quantity":1, "time_left":"LONG", "unit_price":50},                           # missing bid and buyout with quantity = 1
                          {"id":7, "item":{"id":35}, "quantity":5, "time_left":"LONG", "unit_price":50},                           # missing bid and buyout with quantity > 1
                          {"id":8, "item":{"id":35}, "quantity":1, "time_left":"LONG", "buyout":50},                               # missing bid and unit_price with quantity = 1
                          {"id":9, "item":{"id":35}, "quantity":5, "time_left":"LONG", "buyout":250},                              # missing bid and unit_price with quantity > 1
                          {"id":10, "item":{"id":35}, "quantity":1, "time_left":"LONG", "bid":25},                                 # missing unit_price and buyout with quantity = 1
                          {"id":11, "item":{"id":35}, "quantity":5, "time_left":"LONG", "bid":25},                                 # missing unit_price and buyout with quantity > 1
                          {"id":12, "item":{"id":82800}, "quantity":1, "time_left":"LONG", "unit_price":100, "bid":50, "buyout":100, "pet_species_id":17, "pet_quality_id":2, "pet_level":25, "pet_breed_id":2},    # pet
                          {"id":13, "item":{"id":35}, "quantity":5, "time_left":"SHORT", "unit_price":50, "bid":0, "buyout":250},
                          {"id":15, "item":{"id":35}, "quantity":1, "time_left":"MEDIUM", "unit_price":9999999.9999, "bid":0, "buyout":9999999.9999}
                        ]

        values_2 = [
                    [1096, 1, 35, None, 5, 50, "LONG", 25, 250],
                    [1096, 2, 35, None, 5, 50, "LONG", -1, 250],
                    [1096, 3, 35, None, 5, 50, "LONG", 25, -1],
                    [1096, 4, 35, None, 1, 50, "LONG", 25, 50],
                    [1096, 5, 35, None, 5, 50, "LONG", 25, 250],
                    [1096, 6, 35, None, 1, 50, "LONG", -1, 50],
                    [1096, 7, 35, None, 5, 50, "LONG", -1, 250],
                    [1096, 8, 35, None, 1, 50, "LONG", -1, 50],
                    [1096, 9, 35, None, 5, 50, "LONG", -1, 250],
                    [1096, 10, 35, None, 1, 25, "LONG", 25, -1],
                    [1096, 11, 35, None, 5, 5, "LONG", 25, -1],
                    [1096, 12, 82800, {"id":17, "quality_id":2, "level":25, "breed_id":2}, 1, 100, "LONG", 50, 100],
                    [1096, 13, 35, None, 5, 50, "SHORT", 0, 250],
                    [1096, 15, 35, None, 1, 9999999.9999, "MEDIUM", 0, 9999999.9999]
                   ]

        return {"live":live_data, "data_1":auction_data_1, "values_1":values_1, "data_2":auction_data_2, "values_2":values_2, "previous":previous_auctions}




    def test_setAuctionData(self):
        init = self.init()
        previous_auctions = init["previous"]
        live_data = init["live"]
        auction_data = init["data_1"]
        values = init["values_1"]
        insert_data = {}
        update_data = {}
        values_2 = init["values_2"]
        auction_data_2 = init["data_2"]

        # 1st set of auctions
        auctions = setAuctionData(1096, auction_data, live_data, insert_data, update_data, previous_auctions)
        previous_auctions[1096] = live_data["auctions"][1096].copy()
        live_data = init["live"]

        # test if auctions were created
        index = 0
        for auction in auctions:
            self.assertEqual(values[index][1], auction.id)
            self.assertEqual(values[index][2], auction.item_id)
            self.assertEqual(values[index][3], auction.pet_id)
            self.assertEqual(values[index][4], auction.quantity)
            self.assertEqual(values[index][5], auction.unit_price)
            self.assertEqual(values[index][6], auction.time_left)
            self.assertEqual(values[index][7], auction.bid)
            self.assertEqual(values[index][8], auction.buyout)
            self.assertEqual(auction.time_posted, auction.last_updated)
            index += 1

        # test live_data
        self.assertEqual(16, len(live_data["auctions"][1096]))
        self.assertEqual({}, live_data["items"]),
        self.assertEqual({}, live_data["classes"]),
        self.assertEqual({}, live_data["pets"]),
        self.assertEqual({}, live_data["mounts"])

        # test insert_data
        self.assertEqual(16, len(insert_data["auctions"][1096]))
        self.assertEqual(Auction, type(insert_data["auctions"][1096][0]))
        self.assertEqual(1, insert_data["auctions"][1096][0].id)
        self.assertEqual("SHORT", insert_data["auctions"][1096][15].time_left)

        # test_previous_data
        self.assertEqual(16, len(previous_auctions[1096]))

        # test_update_data
        self.assertEqual({}, update_data)


        # 2nd set of auctions
        insert_data = {"auctions":{1096:{}}}
        update_data = {}
        auctions_2 = setAuctionData(1096, auction_data_2, live_data, insert_data, update_data, previous_auctions)

        # test if auctions were updated
        index = 0
        for auction in auctions_2:
            self.assertEqual(values_2[index][1], auction.id)
            self.assertEqual(values_2[index][2], auction.item_id)
            self.assertEqual(values_2[index][3], auction.pet_id)
            self.assertEqual(values_2[index][4], auction.quantity)
            self.assertEqual(values_2[index][5], auction.unit_price)
            self.assertEqual(values_2[index][6], auction.time_left)
            self.assertEqual(values_2[index][7], auction.bid)
            self.assertEqual(values_2[index][8], auction.buyout)
            self.assertEqual(False, auction.time_posted == auctions[auctions_2.index(auction)].last_updated)
            index += 1

        # test live_data
        self.assertEqual(16, len(live_data["auctions"][1096]))
        self.assertEqual({}, live_data["items"]),
        self.assertEqual({}, live_data["classes"]),
        self.assertEqual({}, live_data["pets"]),
        self.assertEqual({}, live_data["mounts"])

        # test insert_data for auctions
        self.assertEqual(0, len(insert_data["auctions"][1096]))

        # test insert_data for sold_auctions
        self.assertEqual(2, len(insert_data["sold_auctions"][1096]))

        # test_previous_data
        self.assertEqual(2, len(previous_auctions[1096]))

        # test_updated_data
        self.assertEqual(14, len(update_data["auctions"][1096]))


    def test_insertAuctions(self):
        init = self.init()
        data_1 = init["data_1"]
        data_2 = init["data_2"]
        live_data = init["live"]
        insert_data = {"auctions":{}, "sold_auctions":{}}
        update_data = {}
        previous_auctions = init["previous"]

        setAuctionData(1096, data_1, live_data, insert_data, update_data, previous_auctions)
        insertAuctions(database, insert_data, previous_auctions)

        # checking inserted auctions into auctionhouses
        data = database.get("SELECT * FROM auctionhouses", True)
        self.assertEqual(16, len(data))

        # checking inserted auctions into soldauctions
        data = database.get("SELECT * FROM soldauctions", True)
        self.assertEqual(0, len(data))

        previous_auctions[1096] = live_data["auctions"][1096].copy()
        live_data = init["live"]
        insert_data = {"auctions":{}, "sold_auctions":{}}
        update_data = {}
        setAuctionData(1096, data_2, live_data, insert_data, update_data, previous_auctions)
        insertAuctions(database, insert_data, previous_auctions)

        # checking inserted auctions into auctionhouses
        data = database.get("SELECT * FROM auctionhouses", True)
        self.assertEqual(16, len(data))

        # checking inserted auctions into soldauctions
        data = database.get("SELECT * FROM soldauctions", True)
        self.assertEqual(4, len(data))


    def test_updateAuctions(self):
        pass



if __name__ == "__main__":
    database = SQL({"type":"SQL", "user":"root", "password":"root", "host":"localhost", "schema":"test"})
    unittest.main()
