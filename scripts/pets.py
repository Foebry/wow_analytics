"""functionality for Pet class"""



class Pet:
    """Pet"""
    def __init__(self, insert_data, update_data, request, pet_id=None, **kwargs):
        """Pet constructor"""
        self.id = pet_id
        if kwargs:
            self.name = kwargs["name"]
            self.type = kwargs["type"]
            self.faction = kwargs["faction"]
            self.source = kwargs["source"]
            self.insert(insert_data)
        else: self.setData(insert_data, update_data, request)

    def setData(self, insert_data, update_data, request):
        data = request.getPetData(self.id)
        data["pet_id"] = data["id"]
        data["type"] = data["battle_pet_type"]["name"]
        if data["is_alliance_only"]: data["faction"] = "Alliance"
        elif data["is_horde_only"]: data["faction"] = "Horde"
        else: data["faction"] = "Factionless"
        data["source"] = data["source"]["name"]
        self.__init__(insert_data, update_data, request, **data)

    def insert(self, insert_data):
        if "pets" in insert_data:
            insert_data["pets"].append(self)
        else: insert_data["pets"] = [self]

    def update(self, update_data):
        if "pets" in update_data:
            update_data["pets"].append(self)
        else: update_data["pets"] = [self]
