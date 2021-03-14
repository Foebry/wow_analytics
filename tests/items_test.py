"""tests for item functionality"""
import unittest
from Wow_Analytics.scripts.items import Item
from Wow_Analytics.scripts.Requests import Request



class ItemTest(unittest.TestCase):

    def init(self):
        ids = [35, 23168, 102936, 55347, 64354, 165577, 30869, 59332, 168704, 21117]
        values = [[35, None, "Bent Staff", "COMMON", 1, 2, 10, 0],
                  [23168, None, "Scorn's Focal Dagger", 'RARE', 20, 2, 15, 0],
                  [102936, None, "Grievous Gladiator's Dragonhide Gloves", 'EPIC', 40, 4, 2, 0],
                  [55347, None, 'Nethergarde Knuckles', 'UNCOMMON', 35, 2, 13, 0],
                  [64354, None, 'Kaldorei Amphora', 'POOR', 1, 15, 4, 0],
                  [165577, None, "Bwonsamdi's Bargain", 'EPIC', 60, 4, 0, 0],
                  [30869, None, 'Howling Wind Bracers', 'EPIC', 32, 4, 3, 0],
                  [59332, None, 'Symbiotic Worm', 'EPIC', 37, 4, 0, 0],
                  [168704, None, 'Dredged Leather Boots', 'EPIC', 76, 4, 2, 0],
                  [21117, None, 'Talisman of Arathor', 'RARE', 27, 4, 0, 0]]
        kwargs = [{"id":values[0][0], "pet":{"id":None}, "name":values[0][2], "quality":values[0][3], "level":values[0][4], "item_class":values[0][5], "item_subclass":values[0][6], "mean_price":values[0][7], "mount":{"id":None}, "type":None, "subtype":None, "sold":0, "price":0, "mean_price":0},
                  {"id":values[1][0], "pet":{"id":None}, "name":values[1][2], "quality":values[1][3], "level":values[1][4], "item_class":values[1][5], "item_subclass":values[1][6], "mean_price":values[1][7], "mount":{"id":None}, "type":None, "subtype":None, "sold":0, "price":0, "mean_price":0},
                  {"id":values[2][0], "pet":{"id":None}, "name":values[2][2], "quality":values[2][3], "level":values[2][4], "item_class":values[2][5], "item_subclass":values[2][6], "mean_price":values[2][7], "mount":{"id":None}, "type":None, "subtype":None, "sold":0, "price":0, "mean_price":0},
                  {"id":values[3][0], "pet":{"id":None}, "name":values[3][2], "quality":values[3][3], "level":values[3][4], "item_class":values[3][5], "item_subclass":values[3][6], "mean_price":values[3][7], "mount":{"id":None}, "type":None, "subtype":None, "sold":0, "price":0, "mean_price":0},
                  {"id":values[4][0], "pet":{"id":None}, "name":values[4][2], "quality":values[4][3], "level":values[4][4], "item_class":values[4][5], "item_subclass":values[4][6], "mean_price":values[4][7], "mount":{"id":None}, "type":None, "subtype":None, "sold":0, "price":0, "mean_price":0},
                  {"id":values[5][0], "pet":{"id":None}, "name":values[5][2], "quality":values[5][3], "level":values[5][4], "item_class":values[5][5], "item_subclass":values[5][6], "mean_price":values[5][7], "mount":{"id":None}, "type":None, "subtype":None, "sold":0, "price":0, "mean_price":0},
                  {"id":values[6][0], "pet":{"id":None}, "name":values[6][2], "quality":values[6][3], "level":values[6][4], "item_class":values[6][5], "item_subclass":values[6][6], "mean_price":values[6][7], "mount":{"id":None}, "type":None, "subtype":None, "sold":0, "price":0, "mean_price":0},
                  {"id":values[7][0], "pet":{"id":None}, "name":values[7][2], "quality":values[7][3], "level":values[7][4], "item_class":values[7][5], "item_subclass":values[7][6], "mean_price":values[7][7], "mount":{"id":None}, "type":None, "subtype":None, "sold":0, "price":0, "mean_price":0},
                  {"id":values[8][0], "pet":{"id":None}, "name":values[8][2], "quality":values[8][3], "level":values[8][4], "item_class":values[8][5], "item_subclass":values[8][6], "mean_price":values[8][7], "mount":{"id":None}, "type":None, "subtype":None, "sold":0, "price":0, "mean_price":0},
                  {"id":values[9][0], "pet":{"id":None}, "name":values[9][2], "quality":values[9][3], "level":values[9][4], "item_class":values[9][5], "item_subclass":values[9][6], "mean_price":values[9][7], "mount":{"id":None}, "type":None, "subtype":None, "sold":0, "price":0, "mean_price":0},
                  ]
        return {"ids":ids, "values":values, "kwargs":kwargs}


    def test_init(self):
        init = self.init()
        ids = init["ids"]
        values = init["values"]
        kwargs = init["kwargs"]
        live_data = {"auctions":{1096:{}}, "items":{}, "classes":{}, "pets":{}, "mounts":{}}
        insert_data = {}
        update_data = {}

        # test without kwargs
        index = 0
        for item_id in ids:
            item = Item(live_data, insert_data, update_data, request, item_id)
            self.assertEqual(values[index][0], item.id)
            self.assertEqual(values[index][1], item.pet_id)
            self.assertEqual(values[index][2], item.name)
            self.assertEqual(values[index][3], item.quality)
            self.assertEqual(values[index][4], item.level)
            self.assertEqual(values[index][5], item.class_id)
            self.assertEqual(values[index][6], item.subclass_id)
            self.assertEqual(values[index][7], item.mean_price)
            index += 1
        # test insert_data
        self.assertEqual(10, len(insert_data["items"]))

        insert_data = {}
        # test with kwargs
        index = 0
        for item_id in ids:
            item = Item(live_data, insert_data, update_data, request, **kwargs[index])
            self.assertEqual(values[index][0], item.id)
            self.assertEqual(values[index][1], item.pet_id)
            self.assertEqual(values[index][2], item.name)
            self.assertEqual(values[index][3], item.quality)
            self.assertEqual(values[index][4], item.level)
            self.assertEqual(values[index][5], item.class_id)
            self.assertEqual(values[index][6], item.subclass_id)
            self.assertEqual(values[index][7], item.mean_price)
            index += 1
        # test insert_data
        self.assertEqual(10, len(insert_data["items"]))



if __name__ == "__main__":
    data = {"id":"2d145be238fc4068a18cd9a2cb7473eb", "secret":"m6eqhka7BWQxVJc9dYn2cO70zLYHE2uo"}
    request = Request(data)
    unittest.main()
