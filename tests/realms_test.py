"""testcases for Realm objects"""

from Wow_Analytics.scripts.realms import Realm
from Wow_Analytics.config import REALMS

import unittest



class RealmTest(unittest.TestCase):
    def init(self):
        return [key for key in REALMS], [REALMS[key] for key in REALMS]

    def test_init(self):
        """testing constructor"""
        names, _ids = self.init()

        index = 0
        for index in range(0, len(realms)):
            _id = _ids[index]
            name = names[index]
            realm = realms[index]

            self.assertEqual(_id, realm.id)
            self.assertEqual(name, realm.name)


if __name__ == '__main__':
    # creating test realm
    realms = [Realm(key, REALMS[key]) for key in REALMS]

    # testing functionality
    unittest.main()
