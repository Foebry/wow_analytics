"""Class and Subclass functionality"""



class Class:
    """Class"""
    def __init__(self, logger, insert_data=None, update_data=None, request=None, class_id=None, **kwargs):
        """Class constructor"""
        new_class = not kwargs
        existing_class = kwargs
        insert_class = existing_class and insert_data is not None

        self.id = class_id

        if insert_class:
            self.name = kwargs["name"]
            self.subclasses = kwargs["subclasses"]
            self.insert(insert_data, logger)

        elif existing_class:
            self.name = kwargs["name"]
            self.subclasses = kwargs["subclasses"]

        elif new_class:
            self.setData(logger, insert_data, update_data, request)


    def setData(self, logger, insert_data, update_data, request):
        data = request.getClassData(self.id, logger)
        data["subclasses"] = {}
        self.__init__(logger, insert_data, update_data, request, **data)


    def insert(self, insert_data, logger):
        set_classes_insert_data = "classes" in insert_data
        unset_classes_insert_data = "classes" not in insert_data

        if set_classes_insert_data: insert_data["classes"].append(self)
        elif unset_classes_insert_data: insert_data["classes"] = [self]
        else: logger.log("class doens't belong anywhere")


    def update(self, update_data, logger):
        set_classes_update_data = "classes" in update_data
        unset_classes_update_data = "classes" not in update_data

        if set_classes_update_data: update_data["classes"].append(self)
        elif unset_classes_update_data: update_data["classes"] = [self]
        else: logger.log("class doesn't belong anywhere")



class Subclass():
    """Subclass"""
    def __init__(self, logger, insert_data=None, update_data=None, request=None, class_id=None, subclass_id=None, **kwargs):
        """Subclass constructor"""
        existing_subclass = kwargs
        insert_subclass = existing_subclass and insert_data is not None
        new_subclass = not kwargs

        self.class_id = class_id
        self.subclass_id = subclass_id

        if insert_subclass:
            self.name = kwargs["name"]
            self.insert(insert_data, logger)

        elif existing_subclass: self.name = kwargs["name"]

        elif new_subclass: self.setData(logger, insert_data, update_data, request)


    def setData(self, logger, insert_data, update_data, request):
        data = request.getSubclassData(self.class_id, self.subclass_id, logger)
        data["name"] = data["display_name"]
        self.__init__(logger, insert_data, update_data, request, **data)


    def insert(self, insert_data, logger):
        set_subclasses_insert_data = "subclasses" in insert_data
        unset_subclasses_insert_data = "subclasses" not in insert_data

        if set_subclasses_insert_data: insert_data["subclasses"].append(self)
        elif unset_subclasses_insert_data: insert_data["subclasses"] = [self]


    def update(self, update_data):
        set_subclasses_update_data = "subclasses" in update_data
        unset_subclasses_update_data = "subclasses" not in update_data

        if set_subclasses_update_data: update_data["subclasses"].append(self)
        elif unset_subclasses_update_data: update_data["subclasses"] = [self]
