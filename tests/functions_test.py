"""tests for functions not directly related to any objects"""
from Wow_Analytics.scripts.functions import setTimePosted
from Wow_Analytics.scripts.functions import setAuctionData
from Wow_Analytics.scripts.auctions import Auction, SoldAuction
from Wow_Analytics.scripts.functions import insertAuctions
from Databases.scripts.SQL import SQL
import unittest
import datetime



class FunctionTest(unittest.TestCase):
    @staticmethod
    def init():
        time = setTimePosted(True)
        update_data = {}
        previous_auctions = {}
        insert_data = {}
        sold_data = {}
        live_data = {"auctions":{1096:{}}}
        insert_auctions = {
            "auctions":{
                    1096: [
                        Auction(live_data, previous_auctions, insert_data, update_data, sold_data, *(1096, 1, 35, 0, 2, 50, "MEDIUM", 49.50, 50, time, time)),
                        Auction(live_data, previous_auctions, insert_data, update_data, sold_data, *(1096, 2, 35, 0, 3, 60, "MEDIUM", 49.50, 120, time, time)),
                        Auction(live_data, previous_auctions, insert_data, update_data, sold_data, *(1096, 3, 35, 0, 4, 70, "MEDIUM", 49.50, 210, time, time)),
                        Auction(live_data, previous_auctions, insert_data, update_data, sold_data, *(1096, 4, 35, 0, 5, 80, "MEDIUM", 49.50, 320, time, time)),
                        Auction(live_data, previous_auctions, insert_data, update_data, sold_data, *(1096, 5, 35, 0, 6, 90, "MEDIUM", 49.50, 450, time, time)),
                        Auction(live_data, previous_auctions, insert_data, update_data, sold_data, *(1096, 6, 35, 0, 6, 100, "MEDIUM", 49.50, 600, time, time)),
                        Auction(live_data, previous_auctions, insert_data, update_data, sold_data, *(1096, 7, 35, 0, 5, 95, "MEDIUM", 49.50, 475, time, time)),
                        Auction(live_data, previous_auctions, insert_data, update_data, sold_data, *(1096, 8, 35, 0, 4, 90, "MEDIUM", 49.50, 360, time, time)),
                        Auction(live_data, previous_auctions, insert_data, update_data, sold_data, *(1096, 9, 35, 0, 3, 85, "MEDIUM", 49.50, 255, time, time)),
                        Auction(live_data, previous_auctions, insert_data, update_data, sold_data, *(1096, 10, 35, 0, 2, 80, "MEDIUM", 49.50, 160, time, time)),
                    ]
                },
            "sold_auctions": {
                1096: [
                    SoldAuction(*(1096, 1, 35, 0, 1, 50, "MEDIUM", 49.50, 50, time, True)),
                    SoldAuction(*(1096, 2, 35, 0, 2, 60, "MEDIUM", 49.50, 120, time, True)),
                    SoldAuction(*(1096, 3, 35, 0, 3, 70, "MEDIUM", 49.50, 210, time, True)),
                    SoldAuction(*(1096, 4, 35, 0, 4, 80, "MEDIUM", 49.50, 320, time, True)),
                    SoldAuction(*(1096, 5, 35, 0, 5, 90, "MEDIUM", 49.50, 450, time, True)),
                    SoldAuction(*(1096, 6, 35, 0, 5, 100, "MEDIUM", 49.50, 600, time, True)),
                    SoldAuction(*(1096, 7, 35, 0, 4, 95, "MEDIUM", 49.50, 475, time, True)),
                    SoldAuction(*(1096, 8, 35, 0, 3, 90, "MEDIUM", 49.50, 360, time, True)),
                    SoldAuction(*(1096, 9, 35, 0, 2, 85, "MEDIUM", 49.50, 255, time, True)),
                    SoldAuction(*(1096, 10, 35, 0, 1, 80, "MEDIUM", 49.50, 160, time, True)),
                    ]
                }
            }
        return {"previous": previous_auctions, "insert":insert_auctions, "update":update_data, "live":live_data, "sold":sold_data}

    def test_setTimePosted(self):
        time_posted = setTimePosted(True)
        self.assertEqual(f"{datetime.datetime.now().date()} 12:30:30.500", time_posted)

    def test_setAuctionData(self):
        init = self.init()
        previous_auctions = init["previous"]
        insert_data = init["insert"]
        update_data = init["update"]
        sold_data = init["sold"]
        live_data = init["live"]

        time = setTimePosted()
        auction_data = [{"id":21, "item":{"id":35}, "quantity":1, "unit_price":50, "time_left":"LONG", "bid":0, "buyout":50},
                        {"id":22, "item":{"id":35}, "quantity":1, "unit_price":50, "time_left":"LONG", "buyout": 50},
                        {"id":23, "item":{"id":35}, "quantity":2, "time_left":"LONG", "bid":0, "buyout":100},
                        {"id":24, "item":{"id":35}, "quantity":2, "time_left":"LONG", "bid":100, "unit_price":50},
                        {"id":25, "item":{"id":35}, "quantity":2, "time_left":"LONG", "unit_price":50},
                        {"id":26, "item":{"id":35}, "quantity":2, "time_left":"LONG", "buyout":100},
                        {"id":27, "item":{"id":35}, "quantity":2, "time_left":"LONG", "bid":50},
                        {"id":28, "item":{"id":8200}, "quantity":1, "time_left":"LONG", "unit_price":100, "bid":0, "buyout":100, "pet_species_id":17, "pet_quality_id":1, "pet_level":25, "pet_breed_id":1}]

        auctions = setAuctionData(1096, auction_data, live_data, previous_auctions, True)

        # test auction_id
        self.assertEqual(21, auctions[0].id)
        self.assertEqual(22, auctions[1].id)
        self.assertEqual(23, auctions[2].id)
        self.assertEqual(24, auctions[3].id)
        self.assertEqual(25, auctions[4].id)
        self.assertEqual(26, auctions[5].id)
        self.assertEqual(27, auctions[6].id)
        self.assertEqual(28, auctions[7].id)

        # test item_id
        self.assertEqual(35, auctions[0].item_id)
        self.assertEqual(35, auctions[3].item_id)
        self.assertEqual(8200, auctions[7].item_id)

        # test_pet_id
        self.assertEqual(None, auctions[0].pet_id)
        self.assertEqual(None, auctions[1].pet_id)
        self.assertEqual({"id":17, "quality_id":1, "level":25, "breed_id":1}, auctions[7].pet_id)

        # test quantity
        self.assertEqual(1, auctions[0].quantity)
        self.assertEqual(2, auctions[2].quantity)
        self.assertEqual(1, auctions[7].quantity)

        # test unit_price
        self.assertEqual(50, auctions[0].unit_price)
        self.assertEqual(50, auctions[2].unit_price)
        self.assertEqual(25, auctions[6].unit_price)
        self.assertEqual(100, auctions[7].unit_price)

        # test time_left
        self.assertEqual("LONG", auctions[0].time_left)
        self.assertEqual("LONG", auctions[4].time_left)
        self.assertEqual("LONG", auctions[6].time_left)

        # test bid
        self.assertEqual(0, auctions[0].bid)
        self.assertEqual(-1, auctions[1].bid)
        self.assertEqual(-1, auctions[4].bid)
        self.assertEqual(-1, auctions[5].bid)

        # test buyout
        self.assertEqual(50, auctions[0].buyout)
        self.assertEqual(-1, auctions[3].buyout)
        self.assertEqual(100, auctions[4].buyout)
        self.assertEqual(-1, auctions[6].buyout)



    def test_updateAuctions(self):
        pass

    def test_insertAuctions(self):
        init = self.init()
        previous_auctions = init["previous"]
        insert_data = init["insert"]
        update_data = init["update"]
        sold_data = init["sold"]
        live_data = init["live"]

        insertAuctions(database, insert_data, previous_auctions)

        # checking inserted auctions into auctionhouses
        query = "SELECT * FROM auctionhouses"
        data = database.get(query, True)
        self.assertEqual(10, len(data))
        self.assertEqual(1096, data[0][0])
        self.assertEqual(2, data[1][1])
        self.assertEqual(35, data[2][2])
        self.assertEqual(0, data[3][3])
        self.assertEqual(6, data[4][4])
        self.assertEqual(100, data[5][5])
        self.assertEqual("MEDIUM", data[6][6])
        self.assertEqual(49.50, data[7][7])
        self.assertEqual(255, data[8][8])
        self.assertEqual(datetime.datetime(2021,3,12,12,30,30,500000), data[9][9])

        # checking inserted auctions into soldauctions
        query = "SELECT * FROM soldauctions"
        data = database.get(query, True)
        self.assertEqual(10, len(data))
        self.assertEqual(1096, data[0][0])
        self.assertEqual(2, data[1][1])
        self.assertEqual(35, data[2][2])
        self.assertEqual(0, data[3][3])
        self.assertEqual(5, data[4][4])
        self.assertEqual(100, data[5][5])
        self.assertEqual("MEDIUM", data[6][6])
        self.assertEqual(49.50, data[7][7])
        self.assertEqual(255, data[8][8])
        self.assertEqual(datetime.datetime(2021,3,12,12,30,30,500000), data[9][9])


if __name__ == "__main__":
    database = SQL({"type":"SQL", "user":"root", "password":"root", "host":"localhost", "schema":"test"})
    unittest.main()
