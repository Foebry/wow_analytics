"main program functionality tests"
from Wow_Analytics.scripts.wow import *
from Wow_Analytics.scripts.auctions import Auction
from Wow_Analytics.scripts.Requests import Request
from Wow_Analytics.scripts.realms import Realm
from Wow_Analytics.scripts.functions import main
from Databases.scripts.SQL import SQL
from configparser import ConfigParser
import unittest



class mainTest(unittest.TestCase):
    def init():
        realm_id = 1096
        values = []
        while len(values) < 50:
            index = random.randrange(0, 100000)
            if index == 82800: pet_id = random.randrange(0, 50000)


    def test_init(realm)


    def test_main(realm):
        pass



if __name__ == "__main__":
    config = ConfigParser()
    config.read('Wow_Analytics.config.ini')
    realms = [init(realm) for realm in config if realm not in ('DEFAULT', 'DATABASE')]
    db = SQL(config['DATABASE'])
    unittest.main()
