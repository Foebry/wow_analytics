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
            if insert_data: self.insert(insert_data)
        else:
            self.id = item_id
            if pet_data:
                self.pet_id = pet_data["id"]
            else: self.pet_id = None
            data = self.setItemData(live_data, insert_data, update_data, request, pet_data)

            if data:
                # new Pet
                if self.pet_id and self.pet_id not in live_data["pets"]:
                    self.Pet = Pet(insert_data, update_data, request, self.pet_id)
                    live_data["pets"][self.pet_id] = self.Pet
                # existing pet
                elif self.pet_id and self.pet_id in live_data["pets"]:
                    self.Pet = live_data["pets"][self.pet_id]

                # new Class
                try:
                    if self.class_id not in live_data["classes"]:
                        self.Class = Class(insert_data, update_data, request, self.class_id)
                        live_data["classes"][self.class_id] = self.Class
                    # existing class
                    else:
                        self.Class = live_data["classes"][self.class_id]
                except Exception as error: logger.write('error', f"line 47 in items.py {error} item {self.id}", type(error))

                # new Subclass
                if self.subclass_id not in live_data["classes"][self.class_id].subclasses:
                    self.Subclass = Subclass(insert_data, update_data, request, self.class_id, self.subclass_id)
                    live_data["classes"][self.class_id].subclasses[self.subclass_id] = self.Subclass
                # existing Subclass
                else:
                    self.Subclass = live_data["classes"][self.class_id].subclasses[self.subclass_id]

                # new Mount
                if self.mount_id and self.mount_id not in live_data["mounts"]:
                    self.Mount = Mount(insert_data, update_data, request, self.mount_id)
                    live_data["mounts"][self.mount_id] = self.Mount
                # existing mount
                elif self.mount_id and self.mount_id in live_data["mounts"]:
                    self.Mount = live_data["mounts"][self.mount_id]


    def setItemData(self, live_data, insert_data, update_data, request, pet_data):
        data = request.getItemData(self.id)
        if data:
            # item is a Mount
            data["mount"] = {}
            data["mount"]["id"] = None
            data["pet"] = {}
            data["pet"]["id"] = None
            data["quality"] = data["quality"]["name"]
            if data["item_subclass"]["name"] == "Mount":
                data["mount"]["id"] = request.getMountIndex(data["name"])
            elif self.id == 82800:
                qualities = {
                0:"POOR", 1:"COMMON", 2:"UNCOMMON", 3:"RARE", 4:"EPIC", 5:"LEGENDARY"}
                data["pet"]["id"] = pet_data["id"]
                data["quality"] = qualities[pet_data["quality"]]
                data["level"] = pet_data["level"]
                temp = request.getPetData(pet_data["id"])
                if "name" in temp: data["name"] = temp["name"]
                else: data["name"] = "Unknown"
            data["item_class"] = data["item_class"]["id"]
            data["item_subclass"] = data["item_subclass"]["id"]
            data["type"] = data["inventory_type"]["type"]
            data["subtype"] = data["inventory_type"]["name"]
            data["sold"] = 0
            data["price"] = 0
            data["mean_price"] = 0
            self.__init__(live_data, insert_data, update_data, request, **data)

        # for testing purposes
        return data


    def insert(self, insert_data):
        """adding Item to be inserted"""
        if "items" in insert_data:
            insert_data["items"].append(self)
        else:
            insert_data["items"] = [self]


    def update(self, update_data):
        """update data for item if mean_price changes"""
        if "items" in update_data:
            update_data["items"].append(self)
        else: update_data["items"] = [self]

        insert_string = "INSERT INTO item_prices (item_id, time, value) VALUES(%s, %s, %s)"%(self.id, f"{datetime.datetime.now()}", self.mean_price)
        if "prices" in insert_data:
            insert_data["prices"].append(insert_string)
        else: insert_data["prices"] = [insert_string]
