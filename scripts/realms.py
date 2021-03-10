"""Realms functionality"""



class Realm:
    """ """

    def __init__(self, data):
        """Realm constructor. Takes in 1 argument
            :arg data: dict:{'id':int, 'name':str}"""
        self.id = data['id']
        self.name = data['name']

        
