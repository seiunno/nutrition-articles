import json
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from flask import Flask
from flask_restful import Resource, Api

def articlescraper():

        json_obj = {}
        json_obj['articles'] = []

        opt = webdriver.ChromeOptions()
        opt.add_argument("--incognito")
        browser = webdriver.Chrome()

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
                        print("error")
                        pass

        with open('articles.json', 'w') as jsonFile:
                json.dump(json_obj, jsonFile)

        browser.close()
        browser.quit()

        return json_obj
        # return jsonFile

app = Flask(__name__)
api = Api(app)

class ArticleList(Resource):
        def get(self):
                article_json = articlescraper()
                print("hello!")
                return article_json, 200

api.add_resource(ArticleList, '/articles')

if __name__ == '__main__':
        app.run(debug=True)
        print("hello?")