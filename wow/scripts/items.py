"""Item functionality"""
import random
import datetime
from Wow_Analytics.scripts.Requests import Request
from Wow_Analytics.scripts.pets import Pet
from Wow_Analytics.scripts.classes import Class, Subclass
from Wow_Analytics.scripts.mounts import Mount



class Item:
    """Item"""
    def __init__(self, logger, live_data=None, insert_data=None, update_data=None, request=None, item_id=None, pet_data=None, **kwargs):
        """constructor for Item class"""
        if kwargs:
            self.id = kwargs["id"]
            self.pet_id = kwargs["pet"]["id"]
            self.mount_id = kwargs["mount"]["id"]
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
        else:
            self.id = item_id
            if pet_data:
                self.pet_id = pet_data["id"]
            else: self.pet_id = None
            data = self.setItemData(logger, live_data, insert_data, update_data, request, pet_data)
            if self.id == 123868:
                print("data for 123686:", data)

            if data:
                # new Pet
                if self.pet_id and self.pet_id not in live_data["pets"]:
                    self.Pet = Pet(logger, insert_data, update_data, request, self.pet_id)
                    live_data["pets"][self.pet_id] = self.Pet
                # existing pet
                elif self.pet_id and self.pet_id in live_data["pets"]:
                    self.Pet = live_data["pets"][self.pet_id]

                # new Class
                if self.class_id not in live_data["classes"]:
                    self.Class = Class(logger, insert_data, update_data, request, self.class_id)
                    live_data["classes"][self.class_id] = self.Class
                # existing class
                else:
                    self.Class = live_data["classes"][self.class_id]

                # new Subclass
                if self.subclass_id not in live_data["classes"][self.class_id].subclasses:
                    self.Subclass = Subclass(logger, insert_data, update_data, request, self.class_id, self.subclass_id)
                    live_data["classes"][self.class_id].subclasses[self.subclass_id] = self.Subclass
                # existing Subclass
                else:
                    self.Subclass = live_data["classes"][self.class_id].subclasses[self.subclass_id]

                # new Mount
                if self.mount_id and self.mount_id not in live_data["mounts"]:
                    self.Mount = Mount(logger, insert_data, update_data, request, self.mount_id)
                    live_data["mounts"][self.mount_id] = self.Mount
                # existing mount
                elif self.mount_id and self.mount_id in live_data["mounts"]:
                    self.Mount = live_data["mounts"][self.mount_id]

                if insert_data is not None:
                    self.insert(insert_data, logger)


    def setItemData(self, logger, live_data, insert_data, update_data, request, pet_data):
        data = request.getItemData(self.id, logger)
        if data:
            # item is a Mount
            data["mount"] = {}
            data["mount"]["id"] = None
            data["pet"] = {}
            data["pet"]["id"] = None
            data["quality"] = data["quality"]["name"]
            if data["item_subclass"]["name"] == "Mount":
                data["mount"]["id"] = request.getMountIndex(data["name"], logger)
            elif self.id == 82800:
                qualities = {
                0:"POOR", 1:"COMMON", 2:"UNCOMMON", 3:"RARE", 4:"EPIC", 5:"LEGENDARY"}
                data["pet"]["id"] = pet_data["id"]
                data["quality"] = qualities[pet_data["quality"]]
                data["level"] = pet_data["level"]
                temp = request.getPetData(pet_data["id"], logger)
                if "name" in temp: data["name"] = temp["name"]
                else: data["name"] = "Unknown"
            data["item_class"] = data["item_class"]["id"]
            data["item_subclass"] = data["item_subclass"]["id"]
            data["type"] = data["inventory_type"]["type"]
            data["subtype"] = data["inventory_type"]["name"]
            data["sold"] = 0
            data["price"] = 0
            data["mean_price"] = 0

            self.__init__(logger, live_data, insert_data, update_data, request, **data)

        # for testing purposes
        return data


    def insert(self, insert_data, logger):
        """adding Item to be inserted"""
        if "items" in insert_data and self.id not in insert_data["items"]:
            insert_data["items"][self.id] = self
        elif "items" not in insert_data:
            insert_data["items"] = {}
            insert_data["items"][self.id] = self


    def update(self, update_data, insert_data, logger):
        """update data for item if mean_price changes"""
        if "items" in update_data:
            update_data["items"].append(self)
        else: update_data["items"] = [self]

        insert_string = "INSERT INTO item_prices (item_id, time, value) VALUES(%s, %s, %s)"%(self.id, f'"{datetime.datetime.now()}"', self.mean_price)
        if "prices" in insert_data:
            insert_data["prices"].append(insert_string)
        else: insert_data["prices"] = [insert_string]
