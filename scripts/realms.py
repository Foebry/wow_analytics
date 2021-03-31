"""Realms functionality"""



class Realm:
    """ """

    def __init__(self, config, realm):
        """Realm constructor. Takes in 1 argument
            :arg data: dict:{'id':int, 'name':str}"""
        self.id = int(config[realm]['id'])
        self.name = config[realm]
        self.credentials = {
            "client_id": config[realm]["client_id"],
            "client_secret": config[realm]["client_secret"]
        }
