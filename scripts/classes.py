"""Class and Subclass functionality"""



class Class:
    """Class"""
    def __init__(self, logger, insert_data=None, update_data=None, request=None, class_id=None, **kwargs):
        """Class constructor"""
        self.id = class_id
        if kwargs:
            self.name = kwargs["name"]
            self.subclasses = kwargs["subclasses"]
            if insert_data is not None:
                self.insert(insert_data, logger)
        else: self.setData(logger, insert_data, update_data, request)

    def setData(self, logger, insert_data, update_data, request):
        data = request.getClassData(self.id, logger)
        data["subclasses"] = {}
        self.__init__(logger, insert_data, update_data, request, **data)

    def insert(self, insert_data, logger):
        if "classes" in insert_data:
            insert_data["classes"].append(self)
        else: insert_data["classes"] = [self]

    def update(self, update_data, logger):
        if "classes" in update_data:
            update_data["classes"].append(self)
        else: update_data["classes"] = [self]


class Subclass():
    """Subclass"""
    def __init__(self, logger, insert_data=None, update_data=None, request=None, class_id=None, subclass_id=None, **kwargs):
        """Subclass constructor"""
        self.class_id = class_id
        self.subclass_id = subclass_id
        if kwargs:
            self.name = kwargs["name"]
            if insert_data is not None:
                self.insert(insert_data, logger)
        else: self.setData(logger, insert_data, update_data, request)

    def setData(self, logger, insert_data, update_data, request):
        data = request.getSubclassData(self.class_id, self.subclass_id, logger)
        data["name"] = data["display_name"]
        self.__init__(logger, insert_data, update_data, request, **data)

    def insert(self, insert_data, logger):
        if "subclasses" in insert_data:
            insert_data["subclasses"].append(self)
        else: insert_data["subclasses"] = [self]

    def update(self, update_data):
        if "subclasses" in update_data:
            update_data["subclasses"].append(self)
        else: update_data["subclasses"] = [self]
