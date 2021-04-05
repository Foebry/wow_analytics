"""testcases for Realm objects"""

from Wow_Analytics.scripts.realms import Realm
from Wow_Analytics.scripts.Requests import Request
from Wow_Analytics import config
from Logger.Logger import *

import unittest
import requests



class RequestTest(unittest.TestCase):


    def init(self):
        """testing constructor"""
        _id = config.CREDENTIALS["client_id"]
        _secret = config.CREDENTIALS["client_secret"]

        self.assertEqual(_id, request.client_id)
        self.assertEqual(_secret, request.client_secret)


    def test_GetAccesToken(self):
        self.assertEqual(str, type(request.getAccesToken(logger)))


    def test_getAuctionData(self):
        self.assertEqual(list, type(request.getAuctionData(1096, logger)))


    def tet_getItemData(self):
        self.assertEqual(dict, type(request.getItemData(19019, logger)))


    def test_getClassData(self):
        self.assertEqual(dict, type(request.getClassData(0, logger)))


    def test_getSubclassData(self):
        self.assertEqual(dict, type(request.getSubclassData(0, 0, logger)))


    def test_getPetData(self):
        self.assertEqual(dict, type(request.getPetData(39, logger)))


    def test_getMountData(self):
        self.assertEqual(dict, type(request.getMountData(6, logger)))


    def test_getMount_id_by_name(self):
        self.assertEqual(522, request.getMount_id_by_name('Sky Golem', logger))


    def test_getPetIndexes(self):
        self.assertEqual(list, type(request.getPetIndex(logger)))


if __name__ == '__main__':

    logger = Logger("E://Projects//Python//Wow_Analytics")
    data = config.CREDENTIALS
    request = Request(data, logger)

    # testing functionality
    unittest.main()
