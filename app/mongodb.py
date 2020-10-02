import pymongo

def test():

    # Create the client
    client = pymongo.MongoClient('mongo', 27017)

    # Connect to our database
    db = client['SeriesDB']

    # Fetch our series collection
    # series_collection = db['series']

    print(db)