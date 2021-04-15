"""Class and Subclass functionality"""



class Class:
    """Class"""
    def __init__(self, logger, insert_data=None, request=None, _id=None, test=False, **kwargs):
        """Class constructor"""
        insert_new_class = kwargs and insert_data is not None
        test_new_class = test
        new_class = not kwargs and insert_data is not None
        rebuild_class = kwargs and not insert_data

        self.id = _id

        if test_new_class: self.kwargs = self.setData(logger, insert_data, request, test)

        elif new_class: self.setData(logger, insert_data, request)

        elif insert_new_class or rebuild_class:
            self.name = kwargs["name"]
            self.subclasses = kwargs["subclasses"]

            if insert_new_class: self.insert(insert_data, logger)


    def setData(self, logger, insert_data, request, test=False):
        data = request.getClassData(self.id, logger)
        if data:
            data["_id"] = data["class_id"]
            data["subclasses"] = {}

            delete = [key for key in data if key not in ["_id", "name", "subclasses"]]

            for key in delete: del(data[key])

            if test: return data

            self.__init__(logger, insert_data, request, **data)


    def insert(self, insert_data, logger):
        set_classes_insert_data = "classes" in insert_data
        unset_classes_insert_data = "classes" not in insert_data

        if set_classes_insert_data: insert_data["classes"].append(self)
        elif unset_classes_insert_data: insert_data["classes"] = [self]



class Subclass():
    """Subclass"""
    def __init__(self, logger, insert_data=None, request=None, class_id=None, subclass_id=None, test=False, **kwargs):
        """Subclass constructor"""
        insert_new_subclass = kwargs and insert_data is not None
        test_new_subclass = test
        new_subclass = not kwargs and insert_data is not None
        rebuild_subclass = kwargs and not insert_data

        self.class_id = class_id
        self.subclass_id = subclass_id

        if test_new_subclass: self.kwargs = self.setData(logger, insert_data, request, test)

        elif new_subclass: self.setData(logger, insert_data, request)

        elif insert_new_subclass or rebuild_subclass:
            self.name = kwargs["name"]

            if insert_new_subclass: self.insert(insert_data, logger)


    def setData(self, logger, insert_data, request, test=False):
        data = request.getSubclassData(self.class_id, self.subclass_id, logger)
        if data:
            data["name"] = data["display_name"]

            delete = [key for key in data if key not in ["class_id", "subclass_id", "name"]]

            for key in delete: del(data[key])

            if test: return data

            self.__init__(logger, insert_data, request, **data)


    def insert(self, insert_data, logger):
        set_subclasses_insert_data = "subclasses" in insert_data
        unset_subclasses_insert_data = "subclasses" not in insert_data

        if set_subclasses_insert_data: insert_data["subclasses"].append(self)
        elif unset_subclasses_insert_data: insert_data["subclasses"] = [self]
