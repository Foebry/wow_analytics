"""Item functionality"""
import random
import datetime
from Requests import Request
from pets import Pet
from classes import Class, Subclass
from mounts import Mount



class Item:
    """Item"""
    def __init__(self, logger, live_data=None, insert_data=None, update_data=None, request=None, _id=None, pet_data=None, test=False, **kwargs):
        """constructor for Item class"""

        insert_new_item = insert_data is not None and not kwargs
        insert_item = insert_data is not None and kwargs
        test_item = test
        rebuild_item = insert_data is None and kwargs

        if test_item:
            self.id = _id
            self.kwargs = self.setData(logger, None, None, None, request, None, test=True)

        elif rebuild_item or insert_item:
            self.pet_id = kwargs["pet"]["_id"]
            self.mount_id = kwargs["mount"]["_id"]
            self.name = kwargs["name"]
            self.level = kwargs["level"]
            self.quality = kwargs["quality"]
            self.class_id = kwargs["item_class"]
            self.subclass_id = kwargs["item_subclass"]
            self.type = kwargs["type"]
            self.subtype = kwargs["subtype"]
            self.sold = kwargs["sold"]
            self.price = kwargs["price"]
            self.mean_price = kwargs["mean_price"]

            if rebuild_item:
                self.id = _id
                self.Pet = kwargs["Pet"]
                self.Mount = kwargs["Mount"]
                self.Class = kwargs["Class"]
                self.Subclass = kwargs["Subclass"]

        elif insert_new_item:
            self.id = _id
            self.Pet = None
            self.Mount = None
            if self.setData(logger, live_data, insert_data, update_data, request, pet_data):
                new_pet = self.id == 82800 and self.pet_id not in live_data["pets"]
                existing_pet = self.id == 82800 and self.pet_id in live_data["pets"]
                new_class = self.class_id not in live_data["classes"]
                existing_class = self.class_id in live_data["classes"]
                new_subclass = self.class_id not in live_data["classes"] or self.subclass_id not in live_data["classes"][self.class_id].subclasses
                existing_subclass = self.class_id in live_data["classes"] and self.subclass_id in live_data["classes"][self.class_id].subclasses
                new_mount = not self.mount_id == 0 and self.mount_id not in live_data["mounts"]
                existing_mount = not self.mount_id == 0 and self.mount_id in live_data["mounts"]

                if new_pet:
                    self.Pet = Pet(logger, insert_data, request, self.pet_id)
                    live_data["pets"][self.pet_id] = self.Pet

                elif existing_pet:
                    self.Pet = live_data["pets"][self.pet_id]

                elif new_mount:
                    self.Mount = Mount(logger, insert_data, request, self.mount_id)
                    live_data["mounts"][self.mount_id] = self.Mount

                elif existing_mount: self.Mount = live_data["mounts"][self.mount_id]

                if new_class:
                    self.Class = Class(logger, insert_data, request, self.class_id)
                    live_data["classes"][self.class_id] = self.Class

                elif existing_class: self.Class = live_data["classes"][self.class_id]

                if new_subclass:
                    self.Subclass = Subclass(logger, insert_data, request, self.class_id, self.subclass_id)
                    live_data["classes"][self.class_id].subclasses[self.subclass_id] = self.Subclass

                elif existing_subclass: self.Subclass = live_data["classes"][self.class_id].subclasses[self.subclass_id]


                self.insert(insert_data, logger)


    def setData(self, logger, live_data, insert_data, update_data, request, pet_data, test=False):
        data = request.getItemData(self.id, logger)
        is_pet = self.id == 82800

        if data:
            is_mount = data["item_subclass"]["name"] == "Mount"

            data["item_class"] = data["item_class"]["id"]
            data["item_subclass"] = data["item_subclass"]["id"]
            data["type"] = data["inventory_type"]["type"]
            data["subtype"] = data["inventory_type"]["name"]
            data["sold"] = 0.0
            data["price"] = 0.0
            data["mean_price"] = 0.0
            data["_id"] = data["id"]
            data["quality"] = data["quality"]["name"]

            if is_pet:
                qualities = {0: "Poor", 1:"Common", 2:"Uncommon", 3:"Rare", 4:"Epic", 5:"Legendary"}
                data["mount"] = {"_id":0}
                data["pet"] = {"_id":pet_data["_id"]}
                data["quality"] = qualities[pet_data["quality"]]
                data["level"] = pet_data["level"]
                data["name"] = request.getPetData(pet_data["_id"], logger)["name"]

            elif is_mount:
                data["mount"] = {"_id":request.getMount_id_by_name(data["name"], logger)}
                data["pet"] = {"_id":0}

            else:
                data["mount"] = {"_id":0}
                data["pet"] = {"_id":0}

            delete = [key for key in data.keys() if key not in ["pet", "mount", "name", "level", "quality", "item_class", "item_subclass", "type", "subtype", "sold", "price", "mean_price", "_id"]]

            for key in delete:
                del(data[key])

            if test: return data

            self.__init__(logger, live_data, insert_data, update_data, request, **data)
            return True


    def insert(self, insert_data, logger):
        """adding Item to be inserted"""
        set_items_insert_data = "items" in insert_data
        unset_items_insert_data = "items" not in insert_data

        if set_items_insert_data: insert_data["items"].append(self)

        elif unset_items_insert_data: insert_data["items"] = [self]


    def update(self, update_data, insert_data, logger):
        """update data for item if mean_price changes"""
        if "items" in update_data:
            update_data["items"].append(self)
        else: update_data["items"] = [self]

        insert_string = "INSERT INTO item_prices (item_id, time, value) VALUES(%s, %s, %s)"%(self.id, f'"{datetime.datetime.now()}"', self.mean_price)
        if "prices" in insert_data:
            insert_data["prices"].append(insert_string)
        else: insert_data["prices"] = [insert_string]
