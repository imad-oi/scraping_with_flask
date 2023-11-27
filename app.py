from flask import Flask, render_template, request
import pandas as pd
from pymongo import MongoClient
import asyncio
# import aiohttp
from utils import get_last_articles, get_categorie_details
from scraping import scrape_this
from sentiment_analys import get_sentiment
from save_to_db import save_to_mongodb,save_dernieres_nouvelles

app = Flask(__name__)


@app.route('/')
def dashboard():
    try:

        barChartLabels, barChartData, doughnutChartLabels, doughnutChartData = get_last_articles()

        client = MongoClient("mongodb://localhost:27017/")
        db = client["LeMatinWebScraping"]
        collection = db["categories"]

        # find just by name and icon fields
        categories = collection.find(
            {}, {"name": 1, "icon": 1, "url": 1, "_id": 0})
        category_list = [category for category in categories]

        return render_template('index.html',
                               categories=category_list, barChartData=barChartData,
                               barChartLabels=barChartLabels, doughnutChartLabels=doughnutChartLabels,
                               doughnutChartData=doughnutChartData)
    except Exception as e:
        print("Error connecting to db:", str(e))
        return None


@app.route('/categorie/<category_name>')
def category(category_name):
    try:
        # transform the category name to lowercase
        category_name = category_name.capitalize()

        category = get_categorie_details(category_name)

        data_donate = {
            "negative": 0,
            "positive": 0,
            "neutral": 0,
        }

        for article in category["data"]:
            sentiment = article["sentiment_category"]
            if sentiment == "negative":
                data_donate["negative"] += 1
            elif sentiment == "positive":
                data_donate["positive"] += 1
            elif sentiment == "neutral":
                data_donate["neutral"] += 1

        if category and "data" in category:
            data_articles = category["data"]

            return render_template('categories.html', category=category, articles=data_articles, data_donate=list(data_donate.values()))
        else:
            return "Category not found or no data available for this category."
    except Exception as e:
        print("Error in category route:", str(e))
        return "An error occurred while processing the request."


@app.route('/scraping')
def scraping():

    return render_template('scrap.html')


@app.route('/scrap_url', methods=['POST'])
def scrap_url():

    url = request.form['url']
    return f"The URL entered \'{url}\' is in process: "  
    # 1- scraping
    base_scrape_url = "https://lematin.ma/emploi"
    number_of_articles = 1000
    articles = []
    if "derniere-heure" in url:
        articles = scrape_this(base_scrape_url, number_of_articles,True)
    else:
        articles = scrape_this(base_scrape_url, number_of_articles)

    df = pd.DataFrame(articles)

    # 2- sentiment analysis
    data_analysed = get_sentiment(df)

    # 3- save to db
    if "derniere-heure" in url:
        save_dernieres_nouvelles(data_analysed)
    else:
        save_to_mongodb(data_analysed)


if __name__ == '__main__':
    app.run()
