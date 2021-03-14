"""Requests testing functionalities"""
import unittest
from Wow_Analytics.scripts.Requests import Request



class RequestTest(unittest.TestCase):

    def test_init(self):
        """testing init method for Request"""
        self.assertEqual(type(str()),type(request.access_token))
        self.assertEqual('2d145be238fc4068a18cd9a2cb7473eb', request.client_id)
        self.assertEqual('m6eqhka7BWQxVJc9dYn2cO70zLYHE2uo', request.client_secret)

    def test_getAuctionData(self):
        """testing getAuctionData method for Request"""
        self.assertEqual(type(list()), type(request.getAuctionData(1096)))

    def test_getItemData(self):
        """testing getItemData method for Request object"""
        # making requests
        response = request.getItemData(35)

        # checking response
        self.assertEqual(type(dict()), type(response))
        self.assertEqual(35, response['id'])
        self.assertEqual("Bent Staff", response["name"])
        self.assertEqual("COMMON",response["quality"]["type"])
        self.assertEqual("Common", response["quality"]["name"])
        self.assertEqual("Weapon", response["item_class"]["name"])
        self.assertEqual("Staff", response["item_subclass"]["name"])

    def test_getClassData(self):
        """testing getClassData for Request object"""
        # making request
        response = request.getClassData(0)

        # checking response
        self.assertEqual(type(dict()), type(response))
        self.assertEqual(0, response["class_id"])
        self.assertEqual("Consumable", response["name"])

    def test_getSubclassData(self):
        """testing getSubclassData for Request object"""
        # making request
        response = request.getSubclassData(0, 0)

        # checking response
        self.assertEqual(type(dict()), type(response))
        self.assertEqual(0, response["class_id"])
        self.assertEqual(0, response["subclass_id"])
        self.assertEqual("Explosives and Devices", response["display_name"])

    def test_getPetData(self):
        """testing getPetData for Request object"""
        # making request
        response = request.getPetData(39)

        # checking response
        self.assertEqual(type(dict()), type(response))
        self.assertEqual(39, response["id"])
        self.assertEqual("Mechanical Squirrel", response["name"])
        self.assertEqual(9, response["battle_pet_type"]["id"])
        self.assertEqual("MECHANICAL", response["battle_pet_type"]["type"])
        self.assertEqual("Mechanical", response["battle_pet_type"]["name"])


    def test_getMountData(self):
        """testing getMountData for Request object"""
        # making request
        response = request.getMountData(6)

        # checking response
        self.assertEqual(type(dict()), type(response))
        self.assertEqual(6, response["id"])
        self.assertEqual("Brown Horse", response["name"]["en_US"])
        self.assertEqual("VENDOR", response["source"]["type"])
        self.assertEqual("Vendor", response["source"]["name"]["en_US"])

    def test_getMountIndex(self):
        response = request.getMountIndex("Sky Golem")

        self.assertEqual(522, response)



if __name__ == '__main__':
    # creating Request object
    data = {
        'id': '2d145be238fc4068a18cd9a2cb7473eb',
        'secret': 'm6eqhka7BWQxVJc9dYn2cO70zLYHE2uo'
    }
    request = Request(data)
    unittest.main()
