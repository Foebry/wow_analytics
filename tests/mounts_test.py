"""mounts test functionality"""
from Wow_Analytics.scripts.mounts import Mount
from Wow_Analytics.scripts.Requests import Request
import unittest
import random




class MountTest(unittest.TestCase):
    def init(self):
        ids = [6, 905, 263, 150, 41, 276, 1239, 65, 479, 424]
        values = [
                    [6, 'Brown Horse', 'Vendor', 'Alliance'],
                    [905, 'Leywoven Flying Carpet', 'Drop', 'Factionless'],
                    [263, 'Black Proto-Drake', 'Vendor', 'Factionless'],
                    [150, 'Thalassian Warhorse', 'Quest', 'Horde'],
                    [41, 'Warhorse', 'Quest', 'Alliance'],
                    [276, 'Armored Snowy Gryphon', 'Vendor', 'Alliance'],
                    [1239, 'X-995 Mechanocat', 'Drop', 'Factionless'],
                    [65, 'Red Skeletal Horse', 'Vendor', 'Horde'],
                    [479, 'Azure Riding Crane', 'Vendor', 'Factionless'],
                    [424, "Vicious Gladiator's Twilight Drake", 'Achievement', 'Factionless'],
                ]
        kwargs = [
                    {"mount_id":values[0][0], "name":values[0][1], "source":values[0][2], "faction":values[0][3]},
                    {"mount_id":values[1][0], "name":values[1][1], "source":values[1][2], "faction":values[1][3]},
                    {"mount_id":values[2][0], "name":values[2][1], "source":values[2][2], "faction":values[2][3]},
                    {"mount_id":values[3][0], "name":values[3][1], "source":values[3][2], "faction":values[3][3]},
                    {"mount_id":values[4][0], "name":values[4][1], "source":values[4][2], "faction":values[4][3]},
                    {"mount_id":values[5][0], "name":values[5][1], "source":values[5][2], "faction":values[5][3]},
                    {"mount_id":values[6][0], "name":values[6][1], "source":values[6][2], "faction":values[6][3]},
                    {"mount_id":values[7][0], "name":values[7][1], "source":values[7][2], "faction":values[7][3]},
                    {"mount_id":values[8][0], "name":values[8][1], "source":values[8][2], "faction":values[8][3]},
                    {"mount_id":values[9][0], "name":values[9][1], "source":values[9][2], "faction":values[9][3]},
                ]
        return ids, values, kwargs

    def test(self):
        ids, values, kwargs = self.init()
        insert_data = {}
        update_data = {}

        # test init without kwargs
        index = 0
        for ID in ids:
            mount = Mount(insert_data, update_data, request, ID)
            self.assertEqual(values[index][0], mount.id)
            self.assertEqual(values[index][1], mount.name)
            self.assertEqual(values[index][2], mount.source)
            self.assertEqual(values[index][3], mount.faction)
            index += 1

            # test insert
            self.assertEqual(index, len(insert_data["mounts"]))

            # test update
            mount.update(update_data)
            self.assertEqual(index, len(update_data["mounts"]))

        insert_data = {}
        update_data = {}

        # test_init with kwargs
        index = 0
        for data in kwargs:
            mount = Mount(insert_data, update_data, request, **data)
            self.assertEqual(values[index][0], mount.id)
            self.assertEqual(values[index][1], mount.name)
            self.assertEqual(values[index][2], mount.source)
            self.assertEqual(values[index][3], mount.faction)
            index += 1

            # test insert
            self.assertEqual(index, len(insert_data["mounts"]))

            # test update
            mount.update(update_data)
            self.assertEqual(index, len(update_data["mounts"]))



if __name__ == "__main__":
    request = Request({"id":"2d145be238fc4068a18cd9a2cb7473eb", "secret":"m6eqhka7BWQxVJc9dYn2cO70zLYHE2uo"})
    unittest.main()
