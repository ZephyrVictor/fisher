from . import web
from flask import render_template

from ..models.gift import Gift
from ..view_models.book import BookViewModel


@web.route('/')
def index():
    recent_gifts = Gift.recent()
    books = [BookViewModel(gift.book) for gift in recent_gifts]
    return render_template('index.html', recent=books)  # 注意这里修改了你的typo，从'rencent'改为了'recent'

@web.route('/personal')
def personal_center():
    pass
