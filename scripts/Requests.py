"""Requests functionalities"""
import requests


class Request():
    """ """
    def __init__(self, data):
        """Request constructor"""
        self.client_id = data['id']
        self.client_secret = data['secret']
        self.access_token = self.getAccesToken()

    def getAccesToken(self):
        """getting access_token"""
        # setting required data
        address = "https://us.battle.net/oauth/token"
        data = {
            'grant_type':'client_credentials',
            'client_id': self.client_id ,
            'client_secret': self.client_secret
        }
        # making request
        response = requests.post(address, data)

        # checking response
        if response.status_code == 200: return response.json()['access_token']
        else: logger.log('error', f'{response.status_code} - response')

    def getAuctionData(self, realm_id):
        """getting auction data"""
        address = f"https://eu.api.blizzard.com/data/wow/connected-realm/{realm_id}/auctions?namespace=dynamic-eu&locale=en_GB&access_token={self.access_token}"
        response = requests.get(address)
        if response.status_code == 200: return response.json()['auctions']
        elif response.status_code == 401:
            self.access_token = self.getAccesToken()
            self.getAuctionData(realm_id)


    def getItemData(self, item):
        """getting item data"""
        address = f"https://eu.api.blizzard.com/data/wow/item/{item}?namespace=static-eu&locale=en_GB&access_token={self.access_token}"
        response = requests.get(address)
        if response.status_code == 200: return response.json()
        elif response.status_code == 401:
            self.access_token = self.getAccesToken()
            self.getItemData(item)

    def getClassData(self, class_id):
        """getting class data"""
        address = f"https://eu.api.blizzard.com/data/wow/item-class/{class_id}?namespace=static-eu&locale=en_GB&access_token={self.access_token}"
        response = requests.get(address)
        if response.status_code == 200: return response.json()
        elif response.status_code == 401:
            self.access_token = self.getAccesToken()
            self.getClassData(class_id)

    def getSubclassData(self, class_id, subclass):
        """getting subclass data"""
        address = f"https://eu.api.blizzard.com/data/wow/item-class/{class_id}/item-subclass/{subclass}?namespace=static-eu&locale=en_GB&access_token={self.access_token}"
        response = requests.get(address)
        if response.status_code == 200: return response.json()
        elif response.status_code == 401:
            self.access_token = self.getAccesToken()
            self.getSubclassData(class_id, subclass)

    def getPetData(self, pet):
        """getting pet data"""
        address = f"https://eu.api.blizzard.com/data/wow/pet/{pet}?namespace=static-eu&locale=en_GB&access_token={self.access_token}"
        response = requests.get(address)
        if response.status_code == 200: return response.json()
        elif response.status_code == 401:
            self.access_token = self.getAccesToken()
            self.getPetData(pet)

    def getMountData(self, mount):
        """getting mount data"""
        address = f"https://eu.api.blizzard.com/data/wow/mount/{mount}?namespace=static-eu&local=en_GB&access_token={self.access_token}"
        response = requests.get(address)
        if response.status_code == 200: return response.json()
        elif response.status_code == 401:
            self.status_code = self.getAccesToken()
            self.getMountData(mount)

    def getMountIndex(self, name):
        """Getting index of mount."""
        address = f"https://eu.api.blizzard.com/data/wow/mount/index?namespace=static-eu&locale=en_GB&access_token={self.access_token}"
        response = requests.get(address)
        if response.status_code == 200:
            response = response.json()["mounts"]
            for index in range(0, len(response)):
                for key in response[index]:
                    if key == "name" and response[index][key] == name:
                        mount_id = response[index]["id"]
                        return mount_id

        elif response.status_code == 401:
            self.status_code = self.getAccesToken()
            self.getMountIndex(name)

    def getPetIndexes(self):
        address = f"https://eu.api.blizzard.com/data/wow/pet/index?namespace=static-eu&locale=en_GB&access_token={self.access_token}"
        response = requests.get(address)
        if response.status_code == 200: return response.json()['pets']
        elif response.status_code == 401:
            self.status_code = self.getAccesToken()
            self.getPetIndexes()
