"""Class and Subclass test functionality"""
from Wow_Analytics.scripts.classes import Class, Subclass
from Wow_Analytics.scripts.Requests import Request
import unittest



class ClassTest(unittest.TestCase):

    def init(self):
        classes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 15, 16, 17, 18]
        values = [
                    [0, "Consumable", {}],
                    [1, "Container", {}],
                    [2, "Weapon", {}],
                    [3, "Gem", {}],
                    [4, "Armor", {}],
                    [5, "Reagent", {}],
                    [6, "Projectile", {}],
                    [7, "Tradeskill", {}],
                    [8, "Item Enhancement", {}],
                    [9, "Recipe", {}],
                    [11, "Quiver", {}],
                    [12, "Quest", {}],
                    [13, "Key", {}],
                    [15, "Miscellaneous", {}],
                    [16, "Glyph", {}],
                    [17, "Battle Pets", {}],
                    [18, "WoW Token", {}]
                ]
        kwargs = [
                    {"class_id":values[0][0], "name":values[0][1], "subclasses":values[0][2]},
                    {"class_id":values[1][0], "name":values[1][1], "subclasses":values[1][2]},
                    {"class_id":values[2][0], "name":values[2][1], "subclasses":values[2][2]},
                    {"class_id":values[3][0], "name":values[3][1], "subclasses":values[3][2]},
                    {"class_id":values[4][0], "name":values[4][1], "subclasses":values[4][2]},
                    {"class_id":values[5][0], "name":values[5][1], "subclasses":values[5][2]},
                    {"class_id":values[6][0], "name":values[6][1], "subclasses":values[6][2]},
                    {"class_id":values[7][0], "name":values[7][1], "subclasses":values[7][2]},
                    {"class_id":values[8][0], "name":values[8][1], "subclasses":values[8][2]},
                    {"class_id":values[9][0], "name":values[9][1], "subclasses":values[9][2]},
                    {"class_id":values[10][0], "name":values[10][1], "subclasses":values[10][2]},
                    {"class_id":values[11][0], "name":values[11][1], "subclasses":values[11][2]},
                    {"class_id":values[12][0], "name":values[12][1], "subclasses":values[12][2]},
                    {"class_id":values[13][0], "name":values[13][1], "subclasses":values[13][2]},
                    {"class_id":values[14][0], "name":values[14][1], "subclasses":values[14][2]},
                    {"class_id":values[15][0], "name":values[15][1], "subclasses":values[15][2]},
                    {"class_id":values[16][0], "name":values[16][1], "subclasses":values[16][2]}
                ]
        return {"classes":classes, "values":values, "kwargs":kwargs}

    def test_init(self):
        init = self.init()
        classes = init["classes"]
        values = init["values"]
        kwargs= init["kwargs"]
        insert_data = {}
        update_data = {}

        # test no kwargs
        index = 0
        for ID in classes:
            test_class = Class(insert_data, update_data, request, ID)
            self.assertEqual(values[index][0], test_class.id)
            self.assertEqual(values[index][1], test_class.name)
            self.assertEqual(values[index][2], test_class.subclasses)
            index += 1

            # test insert_data
            self.assertEqual(index, len(insert_data["classes"]))

            # test update_data
            test_class.update(update_data)
            self.assertEqual(index, len(update_data["classes"]))

        insert_data = {}
        update_data = {}
        # test with kwargs
        index = 0
        for data in kwargs:
            test_class = Class(insert_data, update_data, request, **data)
            self.assertEqual(values[index][0], test_class.id)
            self.assertEqual(values[index][1], test_class.name)
            self.assertEqual(values[index][2], test_class.subclasses)
            index += 1

            # test insert_data
            self.assertEqual(index, len(insert_data["classes"]))

            # test update_data
            test_class.update(update_data)
            self.assertEqual(index, len(update_data["classes"]))



class SubclassTest(unittest.TestCase):

    def init(self):
        subclasses = [(0,0), (0,1), (0,2), (0,3), (0,5), (0,7), (0,8), (0,9)]
        values = [
                    [0, 0, "Explosives and Devices"],
                    [0, 1, "Potion"],
                    [0, 2, "Elixir"],
                    [0, 3, "Flask"],
                    [0, 5, "Food & Drink"],
                    [0, 7, "Bandage"],
                    [0, 8, "Other"],
                    [0, 9, "Vantus Rune"],
        ]
        kwargs = [
                    {"class_id":values[0][0], "subclass_id":values[0][1], "name":values[0][2]},
                    {"class_id":values[1][0], "subclass_id":values[1][1], "name":values[1][2]},
                    {"class_id":values[2][0], "subclass_id":values[2][1], "name":values[2][2]},
                    {"class_id":values[3][0], "subclass_id":values[3][1], "name":values[3][2]},
                    {"class_id":values[4][0], "subclass_id":values[4][1], "name":values[4][2]},
                    {"class_id":values[5][0], "subclass_id":values[5][1], "name":values[5][2]},
                    {"class_id":values[6][0], "subclass_id":values[6][1], "name":values[6][2]},
                    {"class_id":values[7][0], "subclass_id":values[7][1], "name":values[7][2]},
        ]

        return {"values":values, "subclasses":subclasses, "kwargs":kwargs}

    def test_init(self):
        init = self.init()
        values = init["values"]
        subclasses = init["subclasses"]
        kwargs = init["kwargs"]
        insert_data = {}
        update_data = {}

        # test without kwargs
        index = 0
        for row in subclasses:
            class_id = row[0]
            subclass_id = row[1]
            subclass = Subclass(insert_data, update_data, request, class_id, subclass_id)
            self.assertEqual(values[index][0], subclass.class_id)
            self.assertEqual(values[index][1], subclass.subclass_id)
            self.assertEqual(values[index][2], subclass.name)
            index += 1

            # test insert_data
            self.assertEqual(index, len(insert_data["subclasses"]))

            # test update_data
            subclass.update(update_data)
            self.assertEqual(index, len(update_data["subclasses"]))

        insert_data = {}
        update_data = {}
        # test with kwargs
        index = 0
        for data in kwargs:
            subclass = Subclass(insert_data, update_data, request, **data)
            self.assertEqual(values[index][0], subclass.class_id)
            self.assertEqual(values[index][1], subclass.subclass_id)
            self.assertEqual(values[index][2], subclass.name)
            index += 1

            # test insert_data
            self.assertEqual(index, len(insert_data["subclasses"]))

            # test update_data
            subclass.update(update_data)
            self.assertEqual(index, len(update_data["subclasses"]))



if __name__ == "__main__":
    request = Request({"id":"2d145be238fc4068a18cd9a2cb7473eb", "secret":"m6eqhka7BWQxVJc9dYn2cO70zLYHE2uo"})
    unittest.main()
