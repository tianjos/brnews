import requests
import feedparser

from app import models
from app import scheduler
from app import db
from app import app

URLS = {
    'uol': "http://rss.uol.com.br/feed/noticias.xml",
    'globo': "https://g1.globo.com/rss/g1/",
    'folha': "https://feeds.folha.uol.com.br/emcimadahora/rss091.xml"
}


class Fetcher:
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0'
    }
    def __init__(self):
        self.session = requests.Session()
        self.request = requests.Request()
        self.request.headers = self.headers
    
    def fetch(self, url, method='GET'):
        self.request.method = method
        self.request.url = url
        prepare_request = self.session.prepare_request(self.request)
        return self.session.send(prepare_request)

    
class Parser:

    def __init__(self):
        self.urls = URLS
        self.fetcher = Fetcher()
        self.feedparser = feedparser
        self._news = list()
        self.__index = 0
        self.__counter = -1
    
    def __repr__(self):
        return f'<Parser: {self._news}>'
    
    def __len__(self):
        return len(self._news)
    
    # def __iter__(self):
    #     next(self._news)
    
    def __getitem__(self, indice):
        return self._news[indice]

    # def __setitem__(self, indice, value):
    #     self.__index += 1
    #     self._news[indice] = value
    
    def __delitem__(self, indice):
        del self._news[indice]
        self.__index -= 1

    def __iter__(self):
        return iter(self._news)

    def __next__(self):
        return next(self._news)   
    
    def push(self, item):
        self._news.append(item)
        self.__index += 1
    
    def parser(self):
        for site_name, url in self.urls.items():
            try:
                print(f'trying fetch url: {site_name}...')
                response = self.fetcher.fetch(url)
                parsed_content = self.feedparser.parse(response.text)
                for news in parsed_content['entries']:
                    self.push(News.to_json(source=site_name, **news))
            except:
                print(f"could not get rss from {site_name}")

class News:

    @staticmethod
    def to_json(source=None, title=None, link=None, summary=None, published=None, **kwargs):
        return {
            'category': 'geral',
            'source': source,
            'title': title,
            'link': link,
            'summary': summary,
            'publication date': published
        }


def fetch_rss():
    parser = Parser()
    parser.parser()
    for item in parser:
        try:
            source = models.Source.query.filter_by(name=item['source']).first()
            category = models.Category.query.filter_by(name=item['category']).first()
            if not source:
                source = models.Source()
                source.from_json(item['source'])
                db.session.add(source)
                db.session.commit()
            if not category:
                category = models.Category()
                category.from_json(item['category'])
                db.session.add(category)
                db.session.commit()
            if models.News.query.filter_by(title=item['link']).first():
                continue
            else:
                news = models.News()
                news.from_json(**item)
                news.add_source(source)
                news.add_category(category)
                db.session.add(news)
                db.session.commit()
                print('[!] news saved')
        except Exception as e:
            print(f'[*] error to save\n {str(e)} ')

def job1():
    print("Job 1 started.")

def context_fetch_rss():
    with app.app_context():
        fetch_rss()
