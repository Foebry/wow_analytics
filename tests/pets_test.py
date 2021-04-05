"""Pet test functionality"""
from Wow_Analytics.scripts.pets import Pet
from Wow_Analytics.scripts.Requests import Request
from Wow_Analytics.config import CREDENTIALS
from Logger.Logger import Logger

import unittest
import random



class PetTest(unittest.TestCase):
    def init(self):
        pets = request.getPetIndex(logger)
        choises = [pets[x]["id"] for x in range(0,len(pets))]
        _ids = [random.choice(choises) for _ in range(0, 50)]
        data = [{key: request.getPetData(_id, logger)[key] for key in ["id", "name", "battle_pet_type", "is_alliance_only", "is_horde_only", "source"]} for _id in _ids]
        insert_data = {}

        # set value for key "Faction" and delete 2 faction specific keys since we don't need them
        for dict in data:
            if not dict["is_alliance_only"] and not dict["is_horde_only"]: dict["Faction"] = "Factionless"
            elif dict["is_alliance_only"]: dict["Faction"] = "Alliance"
            elif dict["is_horde_only"]: dict["Faction"] = "Horde"
            del(dict["is_alliance_only"])
            del(dict["is_horde_only"])

        # create valid variables to use for pets
        names = [row["name"] for row in data]
        _types = [row["battle_pet_type"]["name"] for row in data]
        factions = ["Alliance" if request.getPetData(_id, logger)["is_alliance_only"] else "Horde" if request.getPetData(_id, logger)["is_horde_only"] else "Factionless" for _id in _ids]
        sources = [row["source"]["name"] for row in data]

        data = [{"_id":_ids[index], "name":names[index], "type":_types[index], "faction":factions[index], "source":sources[index]} for index in range(0, len(_ids))]

        # create new pets using _id
        new_pets = [Pet(logger, insert_data, request, _id) for _id in _ids]

        # generate test_data
        test_data = [Pet(logger, insert_data, request, _id, True).kwargs for _id in _ids]

        return insert_data, new_pets, _ids, names, _types, factions, sources, data, test_data


    def test_init(self):
        insert_data, new_pets, _ids, names, _types, factions, sources, kwargs, _ = args

        # test new pet -> without kwargs
        for index in range(0, len(new_pets)):
            pet = new_pets[index]
            _id = _ids[index]
            name = names[index]
            _type = _types[index]
            faction = factions[index]
            source = sources[index]

            self.assertEquals(_id, pet.id)
            self.assertEquals(name, pet.name)
            self.assertEquals(_type, pet.type)
            self.assertEquals(faction, pet.faction)


    def test_insert(self):
        insert_data, new_pets, *_ = args

        for index in range(0, len(new_pets)):
            pet = new_pets[index]
            self.assertEquals(pet, insert_data["pets"][index])


    def test_setData(self):
        kwargs, test_data = args[-2], args[-1]

        # print(kwargs, "\n"*3, test_data)

        for index in range(0, len(kwargs)):
            self.assertEquals(kwargs[index], test_data[index])



if __name__ == "__main__":
    logger = Logger("E://Projects//Python//Wow_Analytics")
    request = Request(CREDENTIALS, logger)
    args = PetTest().init()

    unittest.main()
