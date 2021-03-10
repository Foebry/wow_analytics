"""testcases for Realm objects"""

from Wow_Analytics.scripts.realms import Realm
import unittest


class RealmTest(unittest.TestCase):

    def test_init(self):
        """testing constructor"""
        self.assertEqual(1096, realm.id)
        self.assertEqual('Scarshield Legion', realm.name)

if __name__ == '__main__':
    # creating test realm
    data = {
        'id': 1096,
        'name': 'Scarshield Legion'
    }
    realm = Realm(data)

    # testing functionality
    unittest.main()
