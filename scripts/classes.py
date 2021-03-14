"""Class and Subclass functionality"""



class Class:
    """Class"""
    def __init__(self, insert_data, update_data, request, class_id=None, **kwargs):
        """Class constructor"""
        if kwargs:
            self.id = class_id
            self.name = kwargs["name"]
            self.subclasses = kwargs["subclasses"]
            self.insert(insert_data)
        else:
            self.id = class_id
            self.setData(insert_data, update_data, request)

    def setData(self, insert_data, update_data, request):
        data = request.getClassData(self.id)
        data["subclasses"] = {}
        self.__init__(insert_data, update_data, request, **data)

    def insert(self, insert_data):
        if "classes" in insert_data:
            insert_data["classes"].append(self)
        else: insert_data["classes"] = [self]

    def update(self, update_data):
        if "classes" in update_data:
            update_data["classes"].append(self)
        else: update_data["classes"] = [self]


class Subclass():
    """Subclass"""
    def __init__(self, insert_data, update_data, request, class_id=None, subclass_id=None, **kwargs):
        """Subclass constructor"""
        self.class_id = class_id
        self.subclass_id = subclass_id
        if kwargs:
            self.name = kwargs["name"]
            self.insert(insert_data)
        else: self.setData(insert_data, update_data, request)

    def setData(self, insert_data, update_data, request):
        data = request.getSubclassData(self.class_id, self.subclass_id)
        data["name"] = data["display_name"]
        self.__init__(insert_data, update_data, request, **data)

    def insert(self, insert_data):
        if "subclasses" in insert_data:
            insert_data["subclasses"].append(self)
        else: insert_data["subclasses"] = [self]

    def update(self, update_data):
        if "subclasses" in update_data:
            update_data["subclasses"].append(self)
        else: update_data["subclasses"] = [self]
