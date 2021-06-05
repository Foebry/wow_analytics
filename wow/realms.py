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
        self.auction_data = None

        query = "select * from responses where realm_id = {}".format(self.id)
        not_set = db.get(query, logger) == None

        if not_set:
            self.insert(db, logger)
            self.last_modified = None
            return

        self.last_modified = db.get(query, logger)[1]



    def update(self, db, logger):
        query = """
                    update responses
                        set previous_response = "{}"
                        where realm_id = {}
                """.format(self.last_modified, self.id)
        db.update(query, logger)


    def insert(self, db, logger):
        query = """
                    insert into responses(realm_id)
                        values({})
                """.format(self.id)

        db.write(query, logger)


    def exportAuctionData(self):
        pass
