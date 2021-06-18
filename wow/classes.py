"""Class and Subclass functionality"""



class Class:
    """Class"""
    def __init__(self, operation=None, request=None, _id=None, test=False, **kwargs):
        """Class constructor"""
        insert_new_class = kwargs and operation is not None
        test_new_class = test
        new_class = not kwargs and operation is not None
        rebuild_class = kwargs and not operation

        self.id = _id

        if test_new_class: self.kwargs = self.setData(operation, request, test)

        elif new_class: self.setData(operation, request)

        elif insert_new_class or rebuild_class:
            self.name = kwargs["name"]
            self.subclasses = kwargs["subclasses"]

            if insert_new_class: self.insert(operation)


    def setData(self, operation, request, test=False):
        data = request.getClassData(self.id)
        if data:
            data["_id"] = data["class_id"]
            data["subclasses"] = {}

            delete = [key for key in data if key not in ["_id", "name", "subclasses"]]

            for key in delete: del(data[key])

            if test: return data

            self.__init__(operation, request, **data)


    def insert(self, operation):
        set_classes_insert_data = "classes" in operation.insert_data
        unset_classes_insert_data = "classes" not in operation.insert_data

        if set_classes_insert_data: operation.insert_data["classes"].append(self)
        elif unset_classes_insert_data: operation.insert_data["classes"] = [self]



class Subclass():
    """Subclass"""
    def __init__(self, operation=None, request=None, class_id=None, subclass_id=None, test=False, **kwargs):
        """Subclass constructor"""
        insert_new_subclass = kwargs and operation is not None
        test_new_subclass = test
        new_subclass = not kwargs and operation is not None
        rebuild_subclass = kwargs and not operation

        self.class_id = class_id
        self.subclass_id = subclass_id

        if test_new_subclass: self.kwargs = self.setData(operation, request, test)

        elif new_subclass: self.setData(operation, request)

        elif insert_new_subclass or rebuild_subclass:
            self.name = kwargs["name"]

            if insert_new_subclass: self.insert(operation)


    def setData(self, operation, request, test=False):
        data = request.getSubclassData(self.class_id, self.subclass_id)
        if data:
            data["name"] = data["display_name"]

            delete = [key for key in data if key not in ["class_id", "subclass_id", "name"]]

            for key in delete: del(data[key])

            if test: return data

            self.__init__(operation, request, **data)


    def insert(self, operation):
        set_subclasses_insert_data = "subclasses" in operation.insert_data
        unset_subclasses_insert_data = "subclasses" not in operation.insert_data

        if set_subclasses_insert_data: operation.insert_data["subclasses"].append(self)
        elif unset_subclasses_insert_data: operation.insert_data["subclasses"] = [self]
