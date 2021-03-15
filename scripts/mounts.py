"""mounts functionality"""



class Mount:
    """Mount"""
    def __init__(self, insert_data, update_data, request, mount_id=None, **kwargs):
        """Mount constructor"""
        self.id = mount_id
        if kwargs:
            self.name = kwargs["name"]
            self.source = kwargs["source"]
            self.faction = kwargs["faction"]
            self.insert(insert_data)
        else: self.getData(insert_data, update_data, request)

    def getData(self, insert_data, update_data, request):
        data = request.getMountData(self.id)
        data["mount_id"] = data["id"]
        data["name"] = data["name"]["en_GB"]
        if "source" not in data: data["source"] = "Unknown"
        else: data["source"] = data["source"]["name"]["en_GB"]
        if "faction" not in data: data["faction"] = "Factionless"
        else: data["faction"] = data["faction"]["name"]["en_GB"]

        self.__init__(insert_data, update_data, request, **data)

    def insert(self, insert_data):
        if "mounts" in insert_data:
            insert_data["mounts"].append(self)
        else: insert_data["mounts"] = [self]

    def update(self, update_data):
        if "mounts" in update_data:
            update_data["mounts"].append(self)
        else: update_data["mounts"] = [self]
