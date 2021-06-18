"""mounts functionality"""



class Mount:
    """Mount"""
    def __init__(self, operation=None, request=None, _id=None, test=False, **kwargs):
        """Mount constructor"""
        insert_new_mount = kwargs and operation is not None and _id
        test_new_mount = test
        new_mount = not kwargs and operation is not None and _id
        rebuild_mount = kwargs and not operation and _id

        if _id:
            self.id = _id

        if test_new_mount: self.kwargs = self.setData(operation, request, test)

        elif new_mount: self.setData(operation, request)

        elif insert_new_mount or rebuild_mount:
            self.name = kwargs["name"]
            self.source = kwargs["source"]
            self.faction = kwargs["faction"]

            if insert_new_mount: self.insert(operation)


    def setData(self, operation, request, test=False):
        data = request.getMountData(self.id)

        if data:
            data["_id"] = data["id"]
            if "source" in data: data["source"] = data["source"]["name"]
            else: data["source"] = "Unknown"

            if "faction" in data: data["faction"] = data["faction"]["name"]
            else: data["faction"] = "Factionless"

            delete = [key for key in data if key not in ["_id", "source", "faction", "name"]]

            for key in delete: del(data[key])

            if test: return data

            self.__init__(operation, request, **data)


    def insert(self, operation):
        set_mounts_insert_data = "mounts" in operation.insert_data
        unset_mounts_insert_data = "mounts" not in operation.insert_data

        if set_mounts_insert_data: operation.insert_data["mounts"].append(self)
        elif unset_mounts_insert_data: operation.insert_data["mounts"] = [self]
