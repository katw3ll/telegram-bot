import pymongo
from bson.dbref import DBRef
import json

# def test():

    # # Connect to our database
    # db = client['SeriesDB']

    # mycol = db['Тест']

    # mydict = { "name": "John", "address": "Highway 37" }

    # x = mycol.insert_one(mydict)
    # print(x.inserted_id)

    

    # print(db)

class DB:
    def __init__(self, hostname='localhost', port=27017):
        self.client = pymongo.MongoClient(hostname, port)
        self.db = self.client['telegram-bot']
        self.main_menu = self.db['main_menu']
    
    def get_main_menu(self):
        return self.main_menu

    def add_category(self, collection_to, name):
        print(self.db.list_collection_names())
        kek = self.db.create_collection(name)
        # print(kek.id
        print(kek)
        print(collection_to['menu'])

    def print(self):
        d = dict((db, [collection for collection in self.client[self.db].list_collection_names()])
             for db in self.client.list_database_names())
        print (json.dumps(d))



if __name__ == '__main__':
    # test()
    db = DB()
    menu = db.get_main_menu()
    db.add_category(menu, 'kek-test-2')