"""Realms functionality"""



class Realm:
    """ """

    def __init__(self, _id, data, db, logger):
        """
            Realm constructor. Takes in 4 argument
                :arg: _id -> int
                :arg: name -> string
                :arg: db -> obj<Database>
                :arg: logger -> obj<Logger>
        """
        self.id = _id
        self.name = data['name']
        self.output = data['file']
        self.database = db
        self.logger = logger
        self.auctions = {}
        self.previous_auctions = {}

        query = "select * from responses where realm_id = {}".format(self.id)
        not_set = db.get(query) is None

        if not_set:
            self.insert()
            self.last_modified = None
            return
        self.last_modified = db.get(query)[1]



    def update(self):
        query = """
                    update responses
                        set previous_response = "{}"
                        where realm_id = {}
                """.format(self.last_modified, self.id)
        self.database.update(query)


    def insert(self):
        query = """
                    insert into responses(realm_id)
                        values({})
                """.format(self.id)

        self.database.write(query)


    def exportAuctionData(self):
        pass



    def setAuctionData(self, response, operation, request, test=False):
        """
            Setting auction data from getAuctionData response. Takes in 3 arguments:
            :arg response,
            :arg operation: <Operation>,
            :arg live_data: dict,
            :arg previous_auctions: dict
        """

        from operations import setTimeSold, setTimePosted
        from auctions import Auction

        auction_data = []

        for auction in response:
            auction_id = auction["id"]
            item_id = auction["item"]["id"]
            pet = {"_id":0}

            if item_id == 82800:
                pet = {"_id":auction["item"]["pet_species_id"], "quality":auction["item"]["pet_quality_id"], "level":auction["item"]["pet_level"], "breed_id":auction["item"]["pet_breed_id"]}

            quantity = auction["quantity"]
            time_left = auction["time_left"]
            time_posted = setTimePosted()
            last_updated = time_posted

            # all are given
            if "unit_price" in auction and "bid" in auction and "buyout" in auction:
                unit_price = auction["unit_price"] / 10000
                bid = auction["bid"] / 10000
                buyout = auction["buyout"] / 10000

            # bid is missing -> bid = -1
            elif "unit_price" in auction and "buyout" in auction and "bid" not in auctions:
                unit_price = auction["unit_price"] / 10000
                buyout = auction["buyout"] / 10000
                bid = -1

            # unit_price is missing -> unit_price = buyout / quantity
            elif "buyout" in auction and "bid" in auction and "unit_price" not in auction:
                buyout = auction["buyout"] / 10000
                bid = auction["bid"] / 10000
                unit_price = buyout / quantity

            # buyout is missing -> buyout = -1
            elif "unit_price" in auction and "bid" in auction and "buyout" not in auction:
                unit_price = auction["unit_price"] / 10000
                bid = auction["bid"] / 10000
                buyout = -1

            # buyout AND bid are missing -> buyout = unit_price*quantity, bid = -1
            elif "unit_price" in auction and "bid" not in auction and "buyout" not in auction:
                unit_price = auction["unit_price"] / 10000
                bid = -1
                buyout = unit_price * quantity

            # bid and unit_price are missing -> unit_price = buyout / quantity, bid = -1
            elif "buyout" in auction and "unit_price" not in auction and "bid" not in auction:
                buyout = auction["buyout"] / 10000
                unit_price = buyout / quantity
                bid = -1

            # buyout AND unit_price are missing -> buyout = -1, unit_price = bid / quantity
            elif "bid" in auction and "unit_price" not in auction and "buyout" not in auction:
                bid = auction["bid"] / 10000
                unit_price = bid / quantity
                buyout = -1

            args = (self, auction_id, item_id, pet, quantity, unit_price, time_left, bid, buyout, time_posted, last_updated)
            auction = Auction(self, operation, request, test, *args)

            print("{}/{} auctions handled".format(len(auction_data), len(response)), end='\r')
            # for testing purposes
            auction_data.append(auction)
        # for testing purposes
        return auction_data
