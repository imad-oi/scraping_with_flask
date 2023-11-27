
from pymongo import MongoClient
from collections import Counter


def get_last_articles():

    client = MongoClient("mongodb://localhost:27017/")
    collection = client.LeMatinWebScraping.dernieres_nouvelles

    articles = collection.find()
    articles

    listCategories = []
    sentiment_categories = []

    for article in articles:
        listCategories.append(article['articl_category'])
        sentiment_categories.append(article['sentiment_category'])

    # doughnut
    compteur_mots_dn = Counter(sentiment_categories)
    doughnutChartLabels = list(compteur_mots_dn.keys())
    doughnutChartData = list(compteur_mots_dn.values())

    # bar
    compteur_mots = Counter(listCategories)
    barChartLabels = list(compteur_mots.keys())
    barChartData = list(compteur_mots.values())

    client.close()

    return barChartLabels, barChartData, doughnutChartLabels, doughnutChartData



def get_categorie_details(name):

    client = MongoClient("mongodb://localhost:27017/")
    db = client["LeMatinWebScraping"]

    # Query the database to find categories that match the given category_name
    categorie = db.categories.find_one(
        {"name": name}, {"data": {"$slice": 100}})
    return categorie
