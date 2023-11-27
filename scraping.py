from bs4 import BeautifulSoup as bs
import requests
import time
import pandas as pd
import random as ran

def scrape_mblock(articl_block,isLastArticles):
    articl_data= {}

    try:
        articl_data['title'] = articl_block.find('a',{"class":"article-title"}).text.strip()
    except:
        articl_data['title'] = None

    try:
        articl_data['description'] = articl_block.find('a',{"class":"article-body"}).text.strip()
    except:
        articl_data['description'] = None

    try:
        articl_data['articl_url'] = articl_block.find('div',{"class":"article-image"}).a.attrs['href']
    except:
        articl_data['articl_url'] = None

    try:
        articl_data['img_url'] = articl_block.find('div',{"class":"article-image"}).a.div.picture.img.attrs['src']
    except:
        articl_data['img_url'] = None

    if isLastArticles:
        try:
            articl_data['articl_category'] = articl_block.find('div',{"class":"article-image"}).a.attrs['href'].split('/')[3]
        except:
            articl_data['articl_category'] = None

    return articl_data
        

def scrape_m_page(articl_blocks,isLastArticles):
    articls = []
    num_blocks = len(articl_blocks)

    for block in range(num_blocks):
        articls.append(scrape_mblock(articl_blocks[block], isLastArticles))
    
    return articls
    



def scrape_this(link,t_count,isLastArticles=False):
    base_url = link       # url of the page to scrape
    target = t_count      # number of articles to scrape
    page_number = 1
    total_pages = 0
    fetched_articles = 0

    article_data = []

    while fetched_articles < target : 
        url = base_url +"?page="+str(page_number)
        print(url)

        source = requests.get(url).text
        soup = bs(source, 'html.parser')
        articl_blocks = soup.find_all('div', class_=['article main-article','article article-left','article article-right'])
        fetched_articles += len(articl_blocks)
        article_data.extend(scrape_m_page(articl_blocks,isLastArticles))
        total_pages = int(soup.find('ul', class_='pager').find_all('li')[-2].a.text)
        current_page = int(soup.find('nav', class_='pagination').ul.find('li', class_='pager-nav active').a.text)
        page_number += 1
        print("current page: ",current_page)
        print("total pages: ",total_pages)
        print("url: ",url)
        print("fetched articles: ",fetched_articles)
        # time.sleep(ran.randint(0,10))

    return article_data