#!/usr/bin/env python3

"""functionality for Pet class"""



class Pet:
    """Pet"""
    def __init__(self, operation=None, request=None, _id=None, test=False, **kwargs):
        """Pet constructor"""
        insert_new_pet = kwargs and operation is not None
        test_new_pet = test
        new_pet = not kwargs and operation is not None
        rebuild_pet = kwargs and not operation

        self.id = _id

        if test_new_pet: self.kwargs = self.setData(operation, request, test)

        elif new_pet: self.setData(operation, request)

        elif insert_new_pet or rebuild_pet:
            self.name = kwargs["name"]
            self.type = kwargs["type"]
            self.faction = kwargs["faction"]
            self.source = kwargs["source"]

            if insert_new_pet: self.insert(operation)


    def setData(self, operation, request, test=False):
        data = request.getPetData(self.id)
        if data:
            data["_id"] = data["id"]
            data["type"] = data["battle_pet_type"]["name"]
            data["source"] = data["source"]["name"]
            data["faction"] = "Factionless"
            if data["is_alliance_only"]: data["faction"] = "Alliance"
            elif data["is_horde_only"]: data["faction"] = "Horde"

            delete = [key for key in data if key not in ["_id", "type", "source", "faction", "name"]]

            for key in delete: del(data[key])

            if test: return data

            self.__init__(operation, request, **data)

    def insert(self, operation):
        set_pets_insert_data = "pets" in operation.insert_data
        unset_pets_insert_data = "pets" not in operation.insert_data

        if set_pets_insert_data: operation.insert_data["pets"].append(self)
        elif unset_pets_insert_data: operation.insert_data["pets"] = [self]
