"""Requests functionalities"""
import requests


class Request():
    """ """
    def __init__(self, data, logger):
        """Request constructor"""
        self.client_id = data['client_id']
        self.client_secret = data['client_secret']
        self.access_token = None
        self.endpoint = None
        self.setAccessToken(logger)



    def setEndpoint(self):

        return "https://eu.api.blizzard.com/data/wow/{}?namespace={}-eu&locale=en_GB{}&access_token=%s"%self.access_token



    def setAccessToken(self, logger):
        """getting access_token"""

        # setting required data
        endpoint = "https://us.battle.net/oauth/token"
        data = {
            'grant_type':'client_credentials',
            'client_id': self.client_id ,
            'client_secret': self.client_secret
        }

        # making request
        try: response = requests.post(endpoint, data=data)
        except requests.exceptions.ConnectionError:
            return self.reconnect(self.getAccesToken, logger, logger)

        # checking response
        self.access_token = self.handleResponse(response, self.setAccessToken, logger, logger, ('access_token',))
        self.endpoint = self.setEndpoint()



    def getAuctionData(self, realm, update_data, db, logger):
        """getting auction data"""
        endpoint = "connected-realm/{}/auctions".format(realm.id)

        print(" "*100, end="\r")
        print("requesting auction data", end="\r")

        try:
            response = requests.get(self.endpoint.format(endpoint, "dynamic", ""))
        except requests.exceptions.ConnectionError:
            return self.reconnect(self.getAuctionData, (realm, update_data, db, logger))


        auctions = self.handleResponse(response, self.getAuctionData, (realm, update_data, db, logger), logger, ('auctions',))

        if auctions:
            if response.headers['last-modified'] == realm.last_modified:
                return []

            realm.last_modified = response.headers['last-modified']

            if 'realms' in update_data:
                update_data["realms"].append(realm)
                return auctions

            update_data['realms'] = [realm]
            return auctions



    def getItemData(self, _id, logger):
        """getting item data"""
        endpoint = "item/{}".format(_id)

        try: response = requests.get(self.endpoint.format(endpoint, "static", ""))
        except requests.exceptions.ConnectionError:
            return self.reconnect(self.getItemData, (_id, logger))
        except requests.exceptions.ChunkedEncodingError:
            print("ChunkedEncodingError for item {}".format(_id))
            quit()

        return self.handleResponse(response, self.getItemData, (_id, logger), logger)



    def getClassData(self, _id, logger):
        """getting class data"""
        endpoint = "item-class/{}".format(_id)

        try: response = requests.get(self.endpoint.format(endpoint, "static", ""))
        except requests.exceptions.ConnectionError:
            return self.reconnect(self.getClassData, (_id, logger))

        return self.handleResponse(response, self.getClassData, (_id, logger), logger)


    def getClassesIndex(self, logger):
        """Retrieving all item_classes"""
        endpoint = "item-class/index"

        try: response = requests.get(self.endpoint.format(endpoint, "static", ""))
        except requests.exceptions.ConnectionError:
            return self.reconnect(self.getClassData, (logger))

        return self.handleResponse(response, self.getClassesIndex, (logger), logger, ("item_classes",))



    def getSubclassData(self, class_id, _id, logger):
        """getting subclass data"""
        endpoint = "item-class/{}/item-subclass/{}".format(class_id, _id)

        try: response = requests.get(self.endpoint.format(endpoint, "static", ""))
        except requests.exceptions.ConnectionError:
            return self.reconnect(self.getSubclassData, (class_id, _id, logger))

        return self.handleResponse(response, self.getSubclassData, (class_id, _id, logger), logger)



    def getPetData(self, _id, logger):
        """getting pet data"""
        endpoint = "pet/{}".format(_id)

        try: response = requests.get(self.endpoint.format(endpoint, "static", ""))
        except requests.exceptions.ConnectionError:
            return self.reconnect(self.getPetData, (_id, logger))

        return self.handleResponse(response, self.getPetData, (_id, logger), logger)



    def getMountData(self, _id, logger):
        """getting mount data"""
        endpoint = "mount/{}".format(_id)

        try: response = requests.get(self.endpoint.format(endpoint, "static", ""))
        except requests.exceptions.ConnectionError:
            return self.reconnect(self.getMountData, (_id, logger))

        return self.handleResponse(response, self.getMountData, (_id, logger), logger)



    def getMount_id_by_name(self, name, logger):
        endpoint = "search/mount"
        extra = "&name.en_US={}&orderby=id&_page=1".format(name.replace(" ", "%20"))

        try: response = requests.get(self.endpoint.format(endpoint, "static", extra))
        except requests.exceptions.ConnectionError:
            return self.reconnect(self.getMount_id_by_name, (name, logger))

        _id = self.handleResponse(response, self.getMount_id_by_name, (name, logger), logger, ('results', 0, 'data', 'id'))

        return _id


    def getMountsIndex(self, logger):
        endpoint = "mount/index"

        try: response = requests.get(self.endpoint.format(endpoint, "static", ""))
        except requests.exceptions.ConnectionError:
            return self.reconnect(self.getMountsIndex, (logger))

        return self.handleResponse(response, self.getMountsIndex, (logger), logger, ("mounts",))



    def getPetsIndex(self, logger):
        endpoint = "pet/index"

        try: response = requests.get(self.endpoint.format(endpoint, "static", ""))
        except requests.exceptions.ConnectionError:
                return self.reconnect(self.getPetsIndex, logger)

        return self.handleResponse(response, self.getPetsIndex, logger, logger, ('pets',))



    def reconnect(self, func, args):
        while True:
            try:
                if requests.get("https://google.com"): return func(*args)
            except requests.exceptions.ConnectionError:
                print("*"*100, end="\r")
                print("Lost internet connection. Waiting for reconnect...", end="\r")



    def waitTillResponsive(unresponsive, args):
        import os

        ips = ('185.60.112.157', '185.60.112.158', '185.60.114.159')
        response = 0

        # already changed this section. Letting old code run to see which server will fail when server unresponsive.
        # response 0 means nothing wrong
        # response 1 meanse something wrong
        while unresponsive:
            for ip in ips: response += os.system("ping {}".format(ip))

            if response == 0: unresponsive = False
            response = 0




    def handleResponse(self, response, func, args, logger, keys=None):
        success = response.status_code == 200
        unauthorized = response.status_code == 401
        not_found = response.status_code == 404
        unresponsive = response.status_code == 504

        if success:
            return self.traverseResponse(response, keys)

        elif unauthorized:
            self.access_token = self.setAccessToken(logger)
            return func(*args)

        elif not_found: return False

        elif unresponsive:
            self.waitTillResponsive(unresponsive)
            return func(*args)

        else: logger.log(msg=f'{response.status_code} - {response}')



    def traverseResponse(self, response, keys):

        data = response.json()

        if keys is None:
            return data

        for key in keys:
            if key not in data:
                return False
            data = data[key]

        return data
