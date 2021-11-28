from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from flask import Flask
from flask_restful import Resource, Api
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

service = Service(ChromeDriverManager().install())

options = Options()
options.add_argument("--headless")
options.add_argument("--incognito")

driver = webdriver.Chrome(
        service=service,
        options=options
)

def articlescraper():
        """
        Scrapes domain Everyday Health for nutrition articles
        """

        json_obj = {}
        json_obj['articles'] = []

        req = requests.get('https://www.everydayhealth.com/diet-nutrition/all-articles/')
        soup = BeautifulSoup(req.content, 'html.parser')

        for each in soup.findAll('article',{'class':'category-index-article category-index-article--regular'}):
                try:
                        title = each.find('a', {'class':'cr-anchor'}).get_text()
                        link = each.find('a', {'class':'cr-anchor'})['href']
                        description = each.find('div',{'class':'category-index-article__dek'}).get_text()
                        no_script = each.find('noscript')
                        if no_script:
                                image = no_script.find('img')
                                if image:
                                        img_src = image['src']

                        entry = {'link':link, 'title':title, 'description':description,'img_src':img_src}

                        json_obj['articles'].append(entry)
                except KeyError:
                        pass

        driver.close()
        driver.quit()

        return json_obj

app = Flask(__name__)
api = Api(app)

class ArticleList(Resource):
        def get(self):
                article_json = articlescraper()
                return article_json, 200

api.add_resource(ArticleList, '/articles')

if __name__ == '__main__':
        app.run(debug=True)