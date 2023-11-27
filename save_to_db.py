import pandas as pd
from pymongo import MongoClient

def save_to_mongodb(df, categorie_name):
    client = MongoClient('localhost', 27017)
    db = client['LeMatinWebScraping']
    collection = db['categories']

    # Convert dataframe to dictionary
    data_dict = df.to_dict("records")

    # Insert collection
    collection.update_one({
        "name": categorie_name},
        {"$set": {"data": data_dict}}
    )

    print("Data saved to MongoDB")
    # Close connection
    client.close()



def save_dernieres_nouvelles(df, collection_name):
    client = MongoClient('localhost', 27017)
    db = client['LeMatinWebScraping']
    collection = db[collection_name]

    # Convert dataframe to dictionary
    data_dict = df.to_dict("records")

    # Insert collection
    collection.insert_many(data_dict)


    print("Data saved to MongoDB")
    # Close connection
    client.close()