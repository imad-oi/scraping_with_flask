from pymongo import MongoClient

def connect_to_db(collection_name):
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["leMatinWebScraping"]  
        collection = db[collection_name]
        print("Connected to db")
        # client.close()    
    except:
        print("Error connecting to db")
        return None
    
    return collection



def find_all_articles():
    collection = connect_to_db("categories")
    articles = collection.find()
    return articles


def find_all_categories():
    pass