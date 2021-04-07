"""functionality for Pet class"""



class Pet:
    """Pet"""
    def __init__(self, logger, insert_data=None, request=None, _id=None, test=False, **kwargs):
        """Pet constructor"""
        insert_new_pet = kwargs and insert_data is not None
        test_new_pet = test
        new_pet = not kwargs and insert_data is not None
        rebuild_pet = kwargs and not insert_data

        self.id = _id

        if test_new_pet: self.kwargs = self.setData(logger, insert_data, request, test)

        elif new_pet: self.setData(logger, insert_data, request)

        elif insert_new_pet or rebuild_pet:
            self.name = kwargs["name"]
            self.type = kwargs["type"]
            self.faction = kwargs["faction"]
            self.source = kwargs["source"]

            if insert_new_pet: self.insert(insert_data, logger)


    def setData(self, logger, insert_data, request, test=False):
        data = request.getPetData(self.id, logger)
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

            self.__init__(logger, insert_data, request, **data)

    def insert(self, insert_data, logger):
        set_pets_insert_data = "pets" in insert_data
        unset_pets_insert_data = "pets" not in insert_data

        if set_pets_insert_data: insert_data["pets"].append(self)
        elif unset_pets_insert_data: insert_data["pets"] = [self]
