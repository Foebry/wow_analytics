"""mounts functionality"""



class Mount:
    """Mount"""
    def __init__(self, logger, insert_data=None, request=None, _id=None, test=False, **kwargs):
        """Mount constructor"""
        insert_new_mount = kwargs and insert_data is not None and _id
        test_new_mount = test
        new_mount = not kwargs and insert_data is not None and _id
        rebuild_mount = kwargs and not insert_data and _id

        if _id:
            self.id = _id

        if test_new_mount: self.kwargs = self.setData(logger, insert_data, request, test)

        elif new_mount: self.setData(logger, insert_data, request)

        elif insert_new_mount or rebuild_mount:
            self.name = kwargs["name"]
            self.source = kwargs["source"]
            self.faction = kwargs["faction"]

            if insert_new_mount: self.insert(insert_data, logger)


    def setData(self, logger, insert_data, request, test=False):
        data = request.getMountData(self.id, logger)

        if data:
            data["_id"] = data["id"]
            if "source" in data: data["source"] = data["source"]["name"]
            else: data["source"] = "Unknown"

            if "faction" in data: data["faction"] = data["faction"]["name"]
            else: data["faction"] = "Factionless"

            delete = [key for key in data if key not in ["_id", "source", "faction", "name"]]

            for key in delete: del(data[key])

            if test: return data

            self.__init__(logger, insert_data, request, **data)


    def insert(self, insert_data, logger):
        set_mounts_insert_data = "mounts" in insert_data
        unset_mounts_insert_data = "mounts" not in insert_data

        if set_mounts_insert_data: insert_data["mounts"].append(self)
        elif unset_mounts_insert_data: insert_data["mounts"] = [self]
