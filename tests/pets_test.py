"""Pet test functionality"""
from Wow_Analytics.scripts.pets import Pet
from Wow_Analytics.scripts.Requests import Request
import unittest
import random



class PetTest(unittest.TestCase):
    def init(self):
        pet_ids = [2680, 1197, 3016, 1662, 1766, 2905, 201, 627, 209, 2681]
        values = [
                [2680, "Zanj'ir Poker", 'Humanoid', "Factionless", 'Drop'],
                [1197, 'Snowy Panda', 'Beast', "Factionless", 'Quest'],
                [3016, 'Fun Guss', 'Elemental', "Factionless", 'Vendor'],
                [1662, 'Cinder Pup', 'Beast', "Factionless", 'Drop'],
                [1766, 'Empowered Manafiend', 'Magic', "Factionless", 'Drop'],
                [2905, 'Dodger', 'Beast', "Factionless", 'Drop'],
                [201, 'Plump Turkey', 'Flying', "Factionless", 'World Event'],
                [627, 'Infected Squirrel', 'Undead', "Factionless", 'Pet Battle'],
                [209, 'Elwynn Lamb', 'Critter', "Factionless", 'Vendor'],
                [2681, 'Murgle', 'Humanoid', "Factionless", 'Drop']
            ]
        kwargs = [
                    {"pet_id":values[0][0], "name":values[0][1], "type":values[0][2], "faction":values[0][3], "source":values[0][4]},
                    {"pet_id":values[1][0], "name":values[1][1], "type":values[1][2], "faction":values[1][3], "source":values[1][4]},
                    {"pet_id":values[2][0], "name":values[2][1], "type":values[2][2], "faction":values[2][3], "source":values[2][4]},
                    {"pet_id":values[3][0], "name":values[3][1], "type":values[3][2], "faction":values[3][3], "source":values[3][4]},
                    {"pet_id":values[4][0], "name":values[4][1], "type":values[4][2], "faction":values[4][3], "source":values[4][4]},
                    {"pet_id":values[5][0], "name":values[5][1], "type":values[5][2], "faction":values[5][3], "source":values[5][4]},
                    {"pet_id":values[6][0], "name":values[6][1], "type":values[6][2], "faction":values[6][3], "source":values[6][4]},
                    {"pet_id":values[7][0], "name":values[7][1], "type":values[7][2], "faction":values[7][3], "source":values[7][4]},
                    {"pet_id":values[8][0], "name":values[8][1], "type":values[8][2], "faction":values[8][3], "source":values[8][4]},
                    {"pet_id":values[9][0], "name":values[9][1], "type":values[9][2], "faction":values[9][3], "source":values[9][4]},
                ]
        return {"ids":pet_ids, "values":values, "kwargs":kwargs}

    def test_init(self):
        init = self.init()
        ids = init["ids"]
        values = init["values"]
        kwargs = init["kwargs"]
        insert_data = {}
        update_data = {}

        # no kwargs
        index = 0
        for id in ids:
            pet = Pet(insert_data, update_data, request, id)
            self.assertEqual(values[index][0], pet.id)
            self.assertEqual(values[index][1], pet.name)
            self.assertEqual(values[index][2], pet.type)
            self.assertEqual(values[index][3], pet.faction)
            self.assertEqual(values[index][4], pet.source)
            index += 1

            # test insert
            self.assertEqual(index, len(insert_data["pets"]))

            # test update
            pet.update(update_data)
            self.assertEqual(index, len(update_data["pets"]))

        insert_data = {}
        update_data = {}

        # with kwargs
        index = 0
        for data in kwargs:
            pet = Pet(insert_data, update_data, request, **data)
            self.assertEqual(values[index][0], pet.id)
            self.assertEqual(values[index][1], pet.name)
            self.assertEqual(values[index][2], pet.type)
            self.assertEqual(values[index][3], pet.faction)
            self.assertEqual(values[index][4], pet.source)
            index += 1

            # test insert
            self.assertEqual(index, len(insert_data["pets"]))

            # test update
            pet.update(update_data)
            self.assertEqual(index, len(update_data["pets"]))


if __name__ == "__main__":
    request = Request({"id":"2d145be238fc4068a18cd9a2cb7473eb", "secret":"m6eqhka7BWQxVJc9dYn2cO70zLYHE2uo"})
    unittest.main()
