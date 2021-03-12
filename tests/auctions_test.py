"""auction tests functionality"""
from Wow_Analytics.scripts.auctions import Auction
import unittest
import datetime



class AuctionTest(unittest.TestCase):

    def test_init(self):
        # testing for auction with *args
        auction_args = Auction(live_data, insert_data, update_data, sold_data, *(1096, 1, 35, 0, 1, 1, "SHORT", -1, 1, now, now))
        self.assertEqual(1096, auction_args.realm_id)
        self.assertEqual(1, auction_args.id)
        self.assertEqual(35, auction_args.item_id)
        self.assertEqual(0, auction_args.pet_id)
        self.assertEqual(1, auction_args.quantity)
        self.assertEqual(1, auction_args.unit_price)
        self.assertEqual("SHORT", auction_args.time_left)
        self.assertEqual(-1, auction_args.bid)
        self.assertEqual(1, auction_args.buyout)
        self.assertEqual(now, auction_args.time_posted)
        self.assertEqual(now, auction_args.last_updated)
        self.assertEqual(1, len(live_data["auctions"][auction_args.realm_id]))
        self.assertEqual(True, auction_args.id in live_data["auctions"][auction_args.realm_id])

        # testing for auction with **kwargs
        auction_kwargs = Auction(live_data, insert_data, update_data, sold_data, **{"realm_id":1096, "id":2, "item_id":35, "pet_id":0, "quantity":1, "unit_price":1, "time_left":"SHORT", "bid":-1, "buyout":1, "time_posted":now, "last_updated":now})
        self.assertEqual(1096, auction_kwargs.realm_id)
        self.assertEqual(2, auction_kwargs.id)
        self.assertEqual(35, auction_kwargs.item_id)
        self.assertEqual(0, auction_kwargs.pet_id)
        self.assertEqual(1, auction_kwargs.quantity)
        self.assertEqual(1, auction_kwargs.unit_price)
        self.assertEqual("SHORT", auction_kwargs.time_left)
        self.assertEqual(-1, auction_kwargs.bid)
        self.assertEqual(1, auction_kwargs.buyout)
        self.assertEqual(now, auction_kwargs.time_posted)
        self.assertEqual(now, auction_kwargs.last_updated)
        self.assertEqual(2, len(live_data["auctions"][auction_kwargs.realm_id]))
        self.assertEqual(True, auction_kwargs.id in live_data["auctions"][auction_kwargs.realm_id])


    def test_Update(self):
        # testing for existing auction
        new_now = datetime.datetime.now()

        # creating 1st auction
        auction = Auction(live_data, insert_data, update_data, sold_data, *(1096, 1, 35, 0, 5, 5, "LONG", -1, 25, now, now))
        self.assertEqual(1, len(live_data["auctions"]))
        self.assertEqual(auction, live_data["auctions"][auction.realm_id][auction.id])

        # created updated auction
        auction_2 = Auction(live_data, insert_data, update_data, sold_data, *(1096, 1, 35, 0, 4, 5, "SHORT", -1, 20, now, new_now))
        self.assertEqual(1, len(live_data["auctions"]))
        self.assertEqual(auction_2, live_data["auctions"][auction.realm_id][auction.id])



class SoldAuctionTest(unittest.TestCase):
    def test_init(self):
        pass

    def test_insert(self):
        pass


if __name__ == '__main__':
    live_data = {"auctions":{1096:{}}}
    insert_data = {}
    update_data = {}
    now = "2021-03-11 12:00:00.000"
    unittest.main()
