"""functionality for Pet class"""



class Pet:
    """Pet"""
    def __init__(self, logger, insert_data=None, update_data=None, request=None, pet_id=None, **kwargs):
        """Pet constructor"""
        self.id = pet_id
        if kwargs:
            self.name = kwargs["name"]
            self.type = kwargs["type"]
            self.faction = kwargs["faction"]
            self.source = kwargs["source"]
        else:
            self.setData(logger, insert_data, update_data, request)

        if insert_data is not None:
            self.insert(insert_data, logger)

    def setData(self, logger, insert_data, update_data, request):
        data = request.getPetData(self.id, logger)
        if data:
            data["pet_id"] = data["id"]
            data["type"] = data["battle_pet_type"]["name"]
            if data["is_alliance_only"]: data["faction"] = "Alliance"
            elif data["is_horde_only"]: data["faction"] = "Horde"
            else: data["faction"] = "Factionless"
            data["source"] = data["source"]["name"]
            self.__init__(logger, insert_data, update_data, request, **data)

    def insert(self, insert_data, logger):
        print("Pet.insert")
        if "pets" in insert_data:
            insert_data["pets"].append(self)
        else: insert_data["pets"] = [self]

    def update(self, update_data):
        if "pets" in update_data:
            update_data["pets"].append(self)
        else: update_data["pets"] = [self]
