# encoding=utf-8
__author__ = 'Zephyr369'
from app.libs.httper import HTTP
from flask import current_app
from pprint import pprint
import json
class Ocean:
    isbn_url = 'https://api.douban.com/v2/book/isbn/{isbn}?apiKey=0ac44ae016490db2204ce0a042db2916' #isbn搜
    keyword_url = 'https://api.douban.com/v2/book/search?q={keyword}&apiKey=0ac44ae016490db2204ce0a042db2916&count={count}'  #keyword 默认搜索结果为2个
    total = 0
    books = []
    def __init__(self):
        self.total = 0
        self.books = []

    def search_by_isbn(self, isbn):
        url = self.isbn_url.format(isbn=isbn)
        result = HTTP.get(url)
        self.__fill_single(result)

    def __fill_single(self, data):
        if data:
            self.total = 1
            self.books.append(data)

    def search_by_keyword(self, keyword, page=1):
        size = current_app.config['PRE_PAGE']
        url = self.keyword_url.format(keyword=keyword,count=5)
        # url = self.keyword_url.format(keyword, current_app.config['PRE_PAGE'], self.calc_start(page))
        result = HTTP.get(url)
        self.__fill_collection(result)

    def __fill_collection(self, data):
        self.total = data['total']
        self.books = data['books']

    @property
    def first(self):
        return self.books[0] if self.total > 0 else None