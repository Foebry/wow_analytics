"""Requests functionalities"""
import requests


class Request():
    """ """
    def __init__(self, realm, logger):
        """Request constructor"""
        self.client_id = realm.credentials["client_id"]
        self.client_secret = realm.credentials['client_secret']
        self.access_token = self.getAccesToken(logger)


    def getAccesToken(self, logger):
        """getting access_token"""
        # setting required data
        address = "https://us.battle.net/oauth/token"
        data = {
            'grant_type':'client_credentials',
            'client_id': self.client_id ,
            'client_secret': self.client_secret
        }
        # making request
        received = False
        while not received:
            try:
                response = requests.post(address, data=data)
                received = True
            except requests.exceptions.ConnectionError:
                print("Lost internet connection. Waiting for reconnect...", end="\r")

        # checking response
        if response.status_code == 200: return response.json()['access_token']
        else: logger.write('error', f'{response.status_code} - response')


    def getAuctionData(self, realm_id, logger):
        """getting auction data"""
        address = f"https://eu.api.blizzard.com/data/wow/connected-realm/{realm_id}/auctions?namespace=dynamic-eu&locale=en_GB&access_token={self.access_token}"
        received = False
        while not received:
            try:
                response = requests.get(address)
                received = True
            except requests.exceptions.ConnectionError:
                print("Lost internet connection. Waiting for reconnect...", end="\r")
        if response.status_code == 200: return response.json()['auctions']
        elif response.status_code == 401:
            self.access_token = self.getAccesToken(logger)
            self.getAuctionData(realm_id, logger)


    def getItemData(self, item, logger):
        """getting item data"""
        address = f"https://eu.api.blizzard.com/data/wow/item/{item}?namespace=static-eu&locale=en_GB&access_token={self.access_token}"
        received = False
        while not received:
            try:
                response = requests.get(address)
                received = True
            except requests.exceptions.ConnectionError:
                print("Lost internet connection. Waiting for reconnect...", end="\r")
        if response.status_code == 200: return response.json()
        elif response.status_code == 401:
            self.access_token = self.getAccesToken(logger)
            self.getItemData(item)
        elif response.status_code == 404: return None
        else: print(response.status_code, "connection error")


    def getClassData(self, class_id, logger):
        """getting class data"""
        address = f"https://eu.api.blizzard.com/data/wow/item-class/{class_id}?namespace=static-eu&locale=en_GB&access_token={self.access_token}"
        received = False
        while not received:
            try:
                response = requests.get(address)
                received = True
            except requests.exceptions.ConnectionError:
                print("Lost internet connection. Waiting for reconnect...", end="\r")
        if response.status_code == 200: return response.json()
        elif response.status_code == 401:
            self.access_token = self.getAccesToken(logger)
            self.getClassData(class_id)
        else: print(response.status_code, "connection error")


    def getSubclassData(self, class_id, subclass, logger):
        """getting subclass data"""
        address = f"https://eu.api.blizzard.com/data/wow/item-class/{class_id}/item-subclass/{subclass}?namespace=static-eu&locale=en_GB&access_token={self.access_token}"
        received = False
        while not received:
            try:
                response = requests.get(address)
                received = True
            except requests.exceptions.ConnectionError:
                print("Lost internet connection. Waiting for reconnect...", end="\r")
        if response.status_code == 200: return response.json()
        elif response.status_code == 401:
            self.access_token = self.getAccesToken(logger)
            self.getSubclassData(class_id, subclass)
        else: print(response.status_code, "connection error")


    def getPetData(self, pet, logger):
        """getting pet data"""
        address = f"https://eu.api.blizzard.com/data/wow/pet/{pet}?namespace=static-eu&locale=en_GB&access_token={self.access_token}"
        received = False
        while not received:
            try:
                response = requests.get(address)
                received = True
            except requests.exceptions.ConnectionError:
                print("Lost internet connection. Waiting for reconnect...", end="\r")
        if response.status_code == 200: return response.json()
        elif response.status_code == 401:
            self.access_token = self.getAccesToken(logger)
            self.getPetData(pet)
        else: print(response.status_code, "connection error")


    def getMountData(self, mount, logger):
        """getting mount data"""
        address = f"https://eu.api.blizzard.com/data/wow/mount/{mount}?namespace=static-eu&local=en_GB&access_token={self.access_token}"
        received = False
        while not received:
            try:
                response = requests.get(address)
                received = True
            except requests.exceptions.ConnectionError:
                print("Lost internet connection. Waiting for reconnect...", end="\r")
        if response.status_code == 200: return response.json()
        elif response.status_code == 401:
            self.status_code = self.getAccesToken(logger)
            self.getMountData(mount)
        else: print(response.status_code, "connection error")


    def getMountIndex(self, name, logger):
        """Getting index of mount."""
        address = f"https://eu.api.blizzard.com/data/wow/mount/index?namespace=static-eu&locale=en_GB&access_token={self.access_token}"
        received = False
        while not received:
            try:
                response = requests.get(address)
                received = True
            except requests.exceptions.ConnectionError:
                print("Lost internet connection. Waiting for reconnect...", end="\r")
        if response.status_code == 200:
            response = response.json()["mounts"]
            for index in range(0, len(response)):
                for key in response[index]:
                    if key == "name" and response[index][key] == name:
                        mount_id = response[index]["id"]
                        return mount_id

        elif response.status_code == 401:
            self.status_code = self.getAccesToken(logger)
            self.getMountIndex(name)
        else: print(response.status_code, "connection error")


    def getPetIndexes(self, logger):
        address = f"https://eu.api.blizzard.com/data/wow/pet/index?namespace=static-eu&locale=en_GB&access_token={self.access_token}"
        received = False
        while not received:
            try:
                response = requests.get(address)
                received = True
            except requests.exceptions.ConnectionError:
                print("Lost internet connection. Waiting for reconnect...", end="\r")
        if response.status_code == 200: return response.json()['pets']
        elif response.status_code == 401:
            self.status_code = self.getAccesToken(logger)
            self.getPetIndexes()
        else: print(response.status_code, "connection error")
