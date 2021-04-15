"""Requests functionalities"""
import requests


class Request():
    """ """
    def __init__(self, data, logger):
        """Request constructor"""
        self.client_id = data['client_id']
        self.client_secret = data['client_secret']
        self.access_token = self.getAccesToken(logger)
        self.endpoint = "https://eu.api.blizzard.com/data/wow/{}?namespace={}-eu&locale=en_GB{}&access_token=%s"%self.access_token



    def getAccesToken(self, logger):
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
        return self.handleResponse(response, self.getAccesToken, logger, logger, ('access_token',))



    def getAuctionData(self, realm_id, logger):
        """getting auction data"""
        endpoint = "connected-realm/{}/auctions".format(realm_id)

        try: response = requests.get(self.endpoint.format(endpoint, "dynamic", ""))
        except requests.exceptions.ConnectionError:
            return self.reconnect(self.getAuctionData, (realm_id, logger))

        return self.handleResponse(response, self.getAuctionData, (realm_id, logger), logger, ('auctions',))



    def getItemData(self, _id, logger):
        """getting item data"""
        endpoint = "item/{}".format(_id)

        try: response = requests.get(self.endpoint.format(endpoint, "static", ""))
        except requests.exceptions.ConnectionError:
            return self.reconnect(self.getItemData, (_id, logger))

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
                print("Lost internet connection. Waiting for reconnect...", end="\r")



    def handleResponse(self, response, func, args, logger, keys=None):
        more_keys = keys and len(keys)>1 and response.status_code == 200
        single_key = keys and response.status_code == 200
        no_keys = not keys and response.status_code == 200
        unauthorized = response.status_code == 401
        not_found = response.status_code == 404

        if more_keys:
            data = response.json()
            for key in keys:
                try: data = data[key]
                except KeyError as error:
                    logger.log(msg=error, type=type(error))
                    return False
                except IndexError as error:
                    logger.log(msg=error, type=type(error))
                    return False
                except Exception as exception:
                    logger.log(msg=exception, type=type(exception))
                    return False
            return data

        elif single_key: return response.json()[keys[0]]
        elif no_keys: return response.json()

        elif unauthorized:
            self.access_token = self.getAccesToken(logger)
            func(*args)

        elif not_found: return False

        else: logger.log(f'{response.status_code} - {response}')
