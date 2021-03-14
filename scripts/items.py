"""Item functionality"""
import random
import datetime
from Wow_Analytics.scripts.Requests import Request
from Wow_Analytics.scripts.pets import Pet
from Wow_Analytics.scripts.classes import Class, Subclass
from Wow_Analytics.scripts.mounts import Mount



class Item:
    """Item"""
    def __init__(self, live_data, insert_data, update_data, request, item_id=None, pet_data=None, **kwargs):
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
            self.insert(insert_data)
        else:
            self.id = item_id
            if pet_data: self.pet_id = pet_data["id"]
            else: self.pet_id = None
            self.setItemData(live_data, insert_data, update_data, request)

            # new Pet
            if self.pet_id and self.pet_id not in live_data["pets"]:
                self.Pet = Pet()
                live_data["pets"][self.pet_id] = self.Pet
            # existing pet
            elif self.pet_id and self.pet_id in live_data["pets"]:
                self.Pet = live_data["pets"][self.pet_id]

            # new Class
            if self.class_id not in live_data["classes"]:
                self.Class = Class()
                live_data["classes"][self.class_id] = self.Class
            # existing class
            else:
                self.Class = live_data["classes"][self.class_id]

            # new Subclass
            if self.subclass_id not in live_data["classes"][self.class_id].subclasses:
                self.Subclass = Subclass()
                live_data["classes"][self.class_id].subclasses[self.subclass_id] = self.Subclass
            # existing Subclass
            else:
                self.Subclass = live_data["classes"][self.class_id].subclasses[self.subclass_id]

            # new Mount
            if self.mount_id not in live_data["mounts"]:
                self.Mount = Mount()
                live_data["mounts"][self.mount_id] = self.Mount
            # existing mount
            else:
                self.Mount = live_data["mounts"][self.mount_id]


    def setItemData(self, live_data, insert_data, update_data, request):
        data = request.getItemData(self.id)
        # item is a Mount
        data["mount"] = {}
        data["mount"]["id"] = None
        data["pet"] = {}
        data["pet"]["id"] = None
        if data["item_subclass"]["name"] == "Mount":
            data["mount"]["id"] = request.getMountIndex(data["name"])
        elif self.id == 82800:
            data["pet"]["id"] = data["pet_species_id"]
        data["quality"] = data["quality"]["type"]
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
