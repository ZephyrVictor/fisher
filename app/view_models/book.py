# encoding=utf-8
__author__ = 'Zephyr369'


class BookViewModel:
    def __init__(self, book):
        self.isbn = book['isbn13' or 'isbn10' or 'isbn']
        self.title = book['title']
        self.publisher = book['publisher']
        self.pages = book['pages'] or ''
        self.author = '、'.join(book['author'])
        self.price = book['price']
        self.summary = book['summary'] or ''
        original_url = book['images']['small']
        # 移除URL中的协议部分
        clean_url = original_url.replace('https://', '').replace('http://', '')
        # 创建weserv的URL参数
        weserv_url = f"https://images.weserv.nl/?url={clean_url}"
        self.image = weserv_url
        self.pubdate = book['pubdate']
        self.binding = book['binding']

    @property
    def intro(self):
        intros = filter(lambda x: True if x else False,
                        [self.author, self.publisher, self.price])
        return '/'.join(intros)


class BookCollection:
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self, yushu_book, keyword):
        self.total = yushu_book.total
        self.keyword = keyword
        self.books = [BookViewModel(book) for book in yushu_book.books]
